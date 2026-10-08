"""Readable functions copied into the standalone Ising II notebook."""
import numpy as np


def total_energy(spins):
    L = len(spins)
    energy = 0
    for i in range(L):
        for j in range(L):
            energy -= spins[i, j] * spins[i, (j + 1) % L]
            energy -= spins[i, j] * spins[(i + 1) % L, j]
    return energy


def delta_energy(spins, i, j):
    L = len(spins)
    neighbors = (spins[(i - 1) % L, j] + spins[(i + 1) % L, j]
                 + spins[i, (j - 1) % L] + spins[i, (j + 1) % L])
    return 2 * spins[i, j] * neighbors


def flip_reference(spins, T, i, j, u):
    trial = spins.copy()
    trial[i, j] *= -1
    change = total_energy(trial) - total_energy(spins)
    if change <= 0 or u < np.exp(-change / T):
        return trial, True
    return spins, False


def flip_local(spins, T, i, j, u):
    change = delta_energy(spins, i, j)
    if change <= 0 or u < np.exp(-change / T):
        spins[i, j] *= -1
        return True
    return False


def replay(initial, T, sites, uniforms, local):
    spins = initial.copy()
    for k in range(len(uniforms)):
        i, j = sites[k]
        if local:
            flip_local(spins, T, i, j, uniforms[k])
        else:
            spins, _ = flip_reference(spins, T, i, j, uniforms[k])
    return spins


def sweep(spins, T, rng):
    L = len(spins)
    for _ in range(spins.size):
        i, j = rng.integers(0, L), rng.integers(0, L)
        u = rng.random()
        flip_local(spins, T, i, j, u)


def run(initial, T, n_equil, n_samples, rng, stride=1):
    if T <= 0:
        raise ValueError("T must be positive.")
    spins = initial.copy()
    for _ in range(n_equil):
        sweep(spins, T, rng)
    energies = np.empty(n_samples)
    magnetizations = np.empty(n_samples)
    for k in range(n_samples):
        for _ in range(stride):
            sweep(spins, T, rng)
        energies[k] = total_energy(spins)
        magnetizations[k] = spins.sum()
    return spins, energies, magnetizations


def measure(energies, magnetizations, N, T):
    energies = energies.astype(np.float64)
    m = magnetizations / N
    e = energies.mean() / N
    abs_m = np.abs(m).mean()
    heat = (np.mean(energies**2) - energies.mean()**2) / (N * T**2)
    binder = 1 - np.mean(m**4) / (3 * np.mean(m**2)**2)
    return np.array([e, abs_m, heat, binder])


def crossings(temperatures, difference):
    found = []
    for k in range(len(temperatures) - 1):
        a, b = difference[k], difference[k + 1]
        if a * b < 0:
            left, right = temperatures[k:k + 2]
            root = left - a * (right - left) / (b - a)
            found.append((left, right, root))
    return found


def temperature_scan(sizes, temperatures, n_runs, n_equil, n_samples, stride):
    samples = np.empty((len(sizes), len(temperatures), n_runs, 2, n_samples),
                       dtype=np.int16)
    for a, L in enumerate(sizes):
        for b, T in enumerate(temperatures):
            for r in range(n_runs):
                seed = 20260917 + 10000 * int(L) + 100 * b + r
                rng = np.random.default_rng(seed)
                initial = np.ones((L, L), dtype=np.int64)
                if r % 2 == 1:
                    initial = rng.choice(np.array([-1, 1]), size=(L, L))
                _, E, M = run(initial, T, n_equil, n_samples, rng, stride)
                samples[a, b, r, 0] = E
                samples[a, b, r, 1] = M
        print("Finished size", L, flush=True)
    return samples


def cool(initial, temperatures, sweeps_per_T, rng):
    if np.min(temperatures) <= 0:
        raise ValueError("Cooling temperatures must be positive.")
    spins = initial.copy()
    best = spins.copy()
    best_energy = total_energy(spins)
    energy = best_energy
    trace = np.empty(len(temperatures) * sweeps_per_T + 1)
    trace[0] = energy
    k = 0
    for T in temperatures:
        for _ in range(sweeps_per_T):
            for _ in range(spins.size):
                i = rng.integers(0, len(spins))
                j = rng.integers(0, len(spins))
                change = delta_energy(spins, i, j)
                if change <= 0 or rng.random() < np.exp(-change / T):
                    spins[i, j] *= -1
                    energy += change
                    if energy < best_energy:
                        best_energy = energy
                        best = spins.copy()
            k += 1
            trace[k] = energy
    return spins, best, best_energy, trace
