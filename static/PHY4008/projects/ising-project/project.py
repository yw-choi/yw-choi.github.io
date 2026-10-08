"""Reproduce the retained Ising project results from the bundled course data.

Run ``python project.py`` inside the extracted teaching package.
The optional --replay check regenerates one complete production stream.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import ising_kernel as k

HERE = Path(__file__).resolve().parent
DATA = HERE / '03_ising_model_2_data.npz'


def configure_plotting():
    for path in (HERE / 'style/fonts').glob('*.otf'):
        font_manager.fontManager.addfont(str(path))
    plt.style.use(HERE / 'style/prl.mplstyle')
    plt.rcParams.update({'font.size': 12, 'axes.labelsize': 13,
                         'legend.fontsize': 11, 'xtick.labelsize': 11,
                         'ytick.labelsize': 11, 'figure.dpi': 110,
                         'text.usetex': False, 'mathtext.fontset': 'stix'})


def load_scan():
    with np.load(DATA, allow_pickle=False) as data:
        scan = {name: data[name].copy() for name in data.files}
    assert scan['samples'].shape == (3, 12, 4, 2, 16000)
    return scan


def reduce_scan(scan):
    values = np.empty(scan['samples'].shape[:3] + (4,))
    for a, L in enumerate(scan['sizes']):
        for b, T in enumerate(scan['temperatures']):
            for r, (E, M) in enumerate(scan['samples'][a, b]):
                values[a, b, r] = k.measure(E, M, int(L)**2, float(T))
    # Each run contributes one estimate, including one Binder estimate.
    return values, values.mean(axis=2), values.std(axis=2, ddof=1) / np.sqrt(values.shape[2])


def independent_energy(state):
    # Explicit bond list, independent of the local-update implementation.
    L = len(state)
    bonds = [((i, j), ((i + 1) % L, j)) for i in range(L) for j in range(L)]
    bonds += [((i, j), (i, (j + 1) % L)) for i in range(L) for j in range(L)]
    return -sum(int(state[a]) * int(state[b]) for a, b in bonds)


def verify_kernel():
    counts = {}
    checks = 0
    for bits in itertools.product((-1, 1), repeat=9):
        state = np.array(bits, dtype=np.int64).reshape(3, 3)
        energy = independent_energy(state)
        assert k.total_energy(state) == energy
        for i, j in itertools.product(range(3), repeat=2):
            trial = state.copy()
            trial[i, j] *= -1
            change = independent_energy(trial) - energy
            assert k.delta_energy(state, i, j) == change
            counts[change] = counts.get(change, 0) + 1
            for T in (1.5, 2.3, 3.5):
                for u in (0., .5, np.nextafter(1., 0.)):
                    actual = state.copy()
                    accepted = k.flip_local(actual, T, i, j, u)
                    expected = change <= 0 or u < np.exp(-change / T)
                    assert accepted == expected
                    assert np.array_equal(actual, trial if expected else state)
                    checks += 1
    return {'states': 512, 'spin_flips': 4608, 'acceptance_checks': checks,
            'delta_energy_counts': {str(a): b for a, b in sorted(counts.items())}}


def replay_illustration():
    """Same draw order as the original Ising I example (seed 42)."""
    initial = np.random.default_rng(42).choice([-1, 1], size=(12, 12))
    final, traces = [], []
    for T in (1.5, 3.5):
        spins, rng = initial.copy(), np.random.default_rng(42)
        trace = [spins.mean()]
        for _ in range(500):
            for _ in range(spins.size):
                i, j = rng.integers(0, 12), rng.integers(0, 12)
                # The original exercise draws a uniform number for every proposal.
                u = rng.random()
                k.flip_local(spins, T, i, j, u)
            trace.append(spins.mean())
        final.append(spins.copy())
        traces.append(trace)
    with np.load(HERE / 'illustration_reference.npz', allow_pickle=False) as ref:
        assert np.array_equal(initial, ref['initial'])
        assert np.array_equal(final, ref['final_states'])
        assert np.array_equal(traces, ref['m_traces'])
    return initial, np.array(final), np.array(traces)


def plot_states(initial, final):
    fig, axes = plt.subplots(1, 3, figsize=(8.5, 3))
    labels = ['Initial state', r'$k_{\mathrm{B}}T/J=1.5$', r'$k_{\mathrm{B}}T/J=3.5$']
    for ax, state, label in zip(axes, [initial, *final], labels):
        ax.imshow(state, cmap='gray', vmin=-1, vmax=1, interpolation='nearest')
        ax.set(xlabel=r'$j$', ylabel=r'$i$', title=label)
        ax.set_xticks([0, 4, 8]); ax.set_yticks([0, 4, 8])
    fig.tight_layout()
    return fig


def plot_energy_check(check):
    fig, ax = plt.subplots(figsize=(5.5, 4))
    x = np.array([int(v) for v in check['delta_energy_counts']])
    ax.plot([-9, 9], [-9, 9], '--', color='black', lw=1)
    ax.plot(x, x, 'o', color='black')
    for v in x:
        ax.annotate(str(check['delta_energy_counts'][str(v)]), (v, v),
                    xytext=(0, 12), textcoords='offset points', ha='center', fontsize=10)
    ax.set(xlabel=r'Full recalculation: $\Delta E/J$', ylabel=r'Local update: $\Delta E/J$',
           xlim=(-10, 10), ylim=(-10, 11))
    ax.set_xticks(x); ax.set_yticks(x)
    fig.tight_layout()
    return fig


def plot_traces(traces):
    fig, ax = plt.subplots(figsize=(7, 3.8))
    for trace, T, style in zip(traces, [1.5, 3.5], ['-', '--']):
        ax.plot(np.arange(len(trace)), trace, style, color='black', lw=.8,
                label=rf'$k_{{\mathrm{{B}}}}T/J={T}$')
    ax.set(xlabel='Sweep', ylabel=r'$m$', xlim=(0, 500), ylim=(-1.05, 1.05))
    ax.legend(loc='lower right'); fig.tight_layout()
    return fig


def plot_production(scan):
    fig, axes = plt.subplots(2, 1, figsize=(7, 5), sharex=True, sharey=True)
    for ax, b in zip(axes, [0, -1]):
        m = scan['samples'][1, b, 0, 1] / 256
        ax.plot(5 * np.arange(1, len(m) + 1), m, color='black', lw=.4)
        ax.set(ylabel=r'$m$', ylim=(-1.05, 1.05), xlim=(0, 80000))
        ax.text(.98, .94, rf'$k_{{\mathrm{{B}}}}T/J={scan["temperatures"][b]}$',
                transform=ax.transAxes, ha='right', va='top')
    axes[-1].set_xlabel('Sweeps after discarded segment')
    fig.tight_layout()
    return fig


def plot_magnetization(scan, mean, se, all_sizes=False):
    fig, ax = plt.subplots(figsize=(7, 4))
    for a in (range(3) if all_sizes else [1]):
        ax.errorbar(scan['temperatures'], mean[a, :, 1], yerr=se[a, :, 1],
                    fmt=['o-', 's--', '^:'][a], color=['black', '#0072B2', '#D55E00'][a],
                    ms=4, capsize=3, label=rf'$L={scan["sizes"][a]}$')
    ax.set(xlabel=r'$k_{\mathrm{B}}T/J$', ylabel=r'$\langle |m|\rangle$',
           xlim=(1.4, 3.6), ylim=(0, 1.05))
    ax.legend(); fig.tight_layout()
    return fig


def plot_run_means(values):
    means = values[1, 6, :, 1]
    center, error = means.mean(), means.std(ddof=1) / np.sqrt(4)
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    ax.axhspan(center - error, center + error, color='0.9', label='Mean ± one SE')
    ax.axhline(center, color='black', lw=1)
    ax.plot(np.arange(1, 5), means, 'o', color='black', label='Independent run mean')
    ax.set(xlabel='Run', ylabel=r'$\langle |m|\rangle$', xticks=[1, 2, 3, 4], xlim=(.5, 4.5))
    ax.legend(loc='best'); fig.tight_layout()
    return fig


def plot_binder(scan, mean, se):
    fig, ax = plt.subplots(figsize=(7, 4))
    for a in range(3):
        ax.errorbar(scan['temperatures'], mean[a, :, 3], yerr=se[a, :, 3],
                    fmt=['o-', 's--', '^:'][a], color=['black', '#0072B2', '#D55E00'][a],
                    ms=4, capsize=3, label=rf'$L={scan["sizes"][a]}$')
    ax.set(xlabel=r'$k_{\mathrm{B}}T/J$', ylabel=r'$U_4$', xlim=(2.19, 2.41), ylim=(.36, .67))
    ax.legend(loc='lower left'); fig.tight_layout()
    return fig


def compile_kernel():
    from numba import njit
    for name in ('total_energy', 'delta_energy', 'flip_local', 'sweep', 'run'):
        f = getattr(k, name)
        if not hasattr(f, 'py_func'):
            setattr(k, name, njit(f))


def exact_benchmark():
    """Reproduce the small-lattice reference check on slide 6."""
    compile_kernel()
    states = np.array(list(itertools.product((-1, 1), repeat=9)), dtype=np.int64).reshape(-1, 3, 3)
    E = np.array([independent_energy(s) for s in states], dtype=float)
    m = states.sum(axis=(1, 2)) / 9
    checks = []
    for T in (1.5, 2.3, 3.5):
        weights = np.exp(-(E - E.min()) / T)
        weights /= weights.sum()
        exact = np.array([weights @ E / 9, weights @ np.abs(m),
            ((weights @ (E**2)) - (weights @ E)**2) / (9 * T**2),
            1 - (weights @ (m**4)) / (3 * (weights @ (m**2))**2)])
        estimates = []
        for r in range(8):
            _, energy, moment = k.run(states[0], T, 1000, 16000,
                                     np.random.default_rng(200 + r), 3)
            estimates.append(k.measure(energy, moment, 9, T))
        estimates = np.array(estimates)
        mean = estimates.mean(axis=0)
        se = estimates.std(axis=0, ddof=1) / np.sqrt(8)
        assert np.all(np.abs(mean - exact) < 6 * se + .001)
        checks.append({'T': T, 'exact': exact.tolist(), 'mean': mean.tolist(), 'se': se.tolist()})
    reference = json.loads((HERE / 'benchmark_reference.json').read_text())['exact_mc_comparisons']
    for actual, expected in zip(checks, reference):
        for quantity in ('exact', 'mean', 'se'):
            np.testing.assert_allclose(actual[quantity], expected[quantity], rtol=0, atol=1e-12)
    return {'L': 3, 'exact_states': 512, 'independent_runs': 8,
            'discarded_sweeps': 1000, 'measurements': 16000, 'stride': 3,
            'seeds': list(range(200, 208)), 'comparisons': checks,
            'matches_retained_benchmark': True}


def production_replay(scan):
    # Optional compiled replay, with the same seed, random start, and draw order.
    compile_kernel()
    L, b, r = 8, 6, 1
    T = float(scan['temperatures'][b])
    rng = np.random.default_rng(20260917 + 10000 * L + 100 * b + r)
    initial = rng.choice(np.array([-1, 1]), size=(L, L))
    _, discard, samples, stride = map(int, scan['parameters'])
    _, E, M = k.run(initial, T, discard, samples, rng, stride)
    assert np.array_equal(E, scan['samples'][0, b, r, 0])
    assert np.array_equal(M, scan['samples'][0, b, r, 1])
    return {'L': L, 'T': T, 'run_index': r, 'measurements': samples,
            'energy_and_magnetization_exactly_match': True}


def verify_reduction(scan, mean, se):
    reference = json.loads((HERE / 'reference_summary.json').read_text())
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == reference['data_sha256']
    np.testing.assert_allclose(mean, reference['mean'], atol=1e-12, rtol=0)
    np.testing.assert_allclose(se, reference['standard_error_across_runs'], atol=1e-12, rtol=0)
    return {'data_sha256': reference['data_sha256'], 'mean_and_se_match': True,
            'max_mean_difference': float(np.max(np.abs(mean - reference['mean']))),
            'max_se_difference': float(np.max(np.abs(se - reference['standard_error_across_runs'])))}


def export_results(scan, values, mean, se, target):
    target = Path(target); target.mkdir(parents=True, exist_ok=True)
    headers = ['L', 'kBT_over_J', 'mean_E_over_NJ', 'SE_E_over_NJ', 'mean_abs_m',
               'SE_abs_m', 'mean_Cv_over_kB', 'SE_Cv_over_kB', 'mean_U4', 'SE_U4']
    with (target / 'observables.csv').open('w', newline='') as f:
        writer = csv.writer(f); writer.writerow(headers)
        for a, L in enumerate(scan['sizes']):
            for b, T in enumerate(scan['temperatures']):
                row = [int(L), float(T)]
                for c in range(4): row.extend([mean[a, b, c], se[a, b, c]])
                writer.writerow(row)
    roots = [{'sizes': scan['sizes'][a:a+2].tolist(),
              'candidates': k.crossings(scan['temperatures'], mean[a, :, 3] - mean[a+1, :, 3])}
             for a in range(2)]
    report = {'parameters': scan['parameters'].tolist(), 'crossings': roots,
              'uncertainty': 'SE across four independent run estimates; not a confidence interval.',
              'validation': verify_reduction(scan, mean, se)}
    (target / 'results.json').write_text(json.dumps(report, indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true', help='Also reproduce one production stream with Numba.')
    parser.add_argument('--benchmark', action='store_true', help='Also reproduce the exact 3-by-3 reference comparison.')
    parser.add_argument('--output', type=Path, default=HERE / 'results')
    args = parser.parse_args()
    configure_plotting()
    scan = load_scan(); values, mean, se = reduce_scan(scan)
    report = export_results(scan, values, mean, se, args.output)
    report['kernel'] = verify_kernel()
    initial, final, traces = replay_illustration()
    report['illustration_exactly_matches'] = True
    figures = {'spin_states': plot_states(initial, final),
               'energy_check': plot_energy_check(report['kernel']),
               'short_trajectories': plot_traces(traces), 'production': plot_production(scan),
               'magnetization_L16': plot_magnetization(scan, mean, se),
               'run_means': plot_run_means(values),
               'magnetization_sizes': plot_magnetization(scan, mean, se, True),
               'binder': plot_binder(scan, mean, se)}
    for name, fig in figures.items():
        fig.savefig(args.output / f'{name}.png', dpi=180, bbox_inches='tight')
        fig.savefig(args.output / f'{name}.svg', bbox_inches='tight')
        plt.close(fig)
    if args.replay: report['production_replay'] = production_replay(scan)
    if args.benchmark:
        benchmark = exact_benchmark()
        (args.output / 'exact_benchmark.json').write_text(json.dumps(benchmark, indent=2))
        report['exact_benchmark_matches'] = benchmark['matches_retained_benchmark']
    (args.output / 'verification.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
