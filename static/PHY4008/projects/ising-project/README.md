# Ising project example

Course companion to [the editable 22-slide presentation](https://docs.google.com/presentation/d/1KAFb_y9PtoIpSW4TPFgb8FJGoKyu-NY-hI6zPfiZNhQ/edit).
The main talk is 15 slides with a suggested duration of 10 minutes; seven slides are backup material.
This is a worked course example, not a new student research result.

## Physics question

How does heating change the mean absolute magnetization of a finite square Ising lattice?
The example compares energy-favored alignment with thermal fluctuations using a model that can be checked exactly at small size.
Metropolis sampling avoids enumerating every configuration on larger lattices.

## Presentation structure

The talk follows the [Presentation Guidelines](https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit):

| Main slides | Part | Suggested time |
|---|---|---|
| 1–3 | Physics question and motivation | 1 minute |
| 4–7 | Model and numerical method | 2 minutes |
| 8–10 | Results and validation | 4 minutes |
| 11–12 | Physical interpretation and limitations | 2 minutes |
| 13–15 | Outlook and Summary | 1 minute |

Slides 16–22 are backup material. Explain each figure in the order axes, comparison, trend, physical meaning.
The opening uses real-material photographs, followed by the physics question, lattice assumptions, energy, magnetization, and the full simulation workflow. Simulation results begin on slide 8.
The final slides propose heat-capacity analysis, susceptibility from weak-field response, spin animations, and spatial correlations.
Slides 13–14 present the response-function and spatial-correlation outlook; slide 15 closes with the study, finding, and further work.
The notes provide speaking cues rather than a script. Q&A is outside this suggested allocation.

## Open and run

1. Extract the complete ZIP. Keep all files in the same folder.
2. Open `index.html` for the executed notebook, including equations and figures. It works offline.
3. For editable code, open `ising_project_example.ipynb` in Jupyter or VS Code and select a Python 3.12 kernel.
4. Use Restart Kernel and Run All. The notebook loads the bundled production data and reruns a short spin example.

Create an environment outside a synced Drive folder, then install the tested dependencies:

```sh
python3.12 -m venv /path/to/ising-venv
# macOS/Linux
source /path/to/ising-venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install jupyterlab
python -m jupyter lab
```

On Windows, activate with `\path\to\ising-venv\Scripts\activate` instead.
After starting Jupyter, navigate to the extracted package folder.

For a script-only run, execute `python project.py`. It saves tables, plots, and verification results in `results/`.
The optional `python project.py --replay` also regenerates one complete production stream using Numba.
Run `python project.py --benchmark` to regenerate the exact small-lattice comparison on slide 9.
Use `python project.py --replay --benchmark` for both checks; the benchmark is saved in `results/exact_benchmark.json`.
The first compiled call may take longer. Python 3.12 and package versions are recorded in `requirements.txt`.

## Files

- `ising_project_example.ipynb`: editable, executed notebook.
- `index.html`: offline reading copy with code and outputs.
- `project.py`, `ising_kernel.py`: analysis, plots, and the original course simulation functions.
- `03_ising_model_2_data.npz`: original saved production scan, unchanged.
- `illustration_reference.npz`: the retained 12-by-12, 500-sweep demonstration for exact replay checks.
- `reference_summary.json`: retained slide values used for comparison, not the source of recalculated results.
- `results/`: regenerated CSV, SVG/PNG figures, and numerical checks.
- `speaker_notes.md`: the existing Korean presentation notes.
- `manifest.json`: SHA-256 checksums and source provenance.

## Evidence and limits

The saved production scan contains sizes 8, 16, and 32; 12 temperatures; four runs per temperature;
8,000 discarded sweeps; and 16,000 measurements per run separated by five sweeps.
Even-numbered zero-based run indices start aligned; odd indices start random.
Each run has a separate random stream. The main talk uses size 16.
The production seed is `20260917 + 10000 * L + 100 * b + r`, where `b` is the zero-based temperature index and `r` is the zero-based run index.
The separate exact benchmark uses a 3-by-3 periodic lattice, all 512 configurations, eight Monte Carlo runs with seeds 200–207,
1,000 discarded sweeps, 16,000 measurements, and stride 3. Its initial state is all down.
Its exact means and Monte Carlo estimates match `benchmark_reference.json`; these settings differ from the production scan.
Production error bars are standard errors across four run estimates. They do not include equilibration bias or finite-size effects.
The two 500-sweep trajectories illustrate the dynamics and do not establish equilibration.
Binder crossings near 2.26 are finite-size, interpolated estimates. The sampled 2.25–2.30 bracket is not a confidence interval.
The notebook reproduces the existing evidence; the longer convergence tests discussed in the talk remain future work.

## References and AI assistance

OpenAI Codex provided substantial assistance with the talk reorganization, English wording, companion notebook,
figure-generation code, and automated checks. The production data and original simulation kernel were reused unchanged;
new companion code connects those sources to the presentation and reproduces its validation results.
This is an instructor-provided worked example and does not represent independent student research.
Checks performed: fresh-kernel execution, full small-lattice enumeration, controlled accept/reject decisions,
exact-benchmark comparison, saved-stream replay, file hashes, and native slide and offline HTML inspection.
AI assistance does not replace the presenter's responsibility to understand the model, code, results, and limitations.

## Motivation image sources

- NdFeB domains: Gorchy, [Kerr microscopy image](https://commons.wikimedia.org/wiki/File:NdFeB-Domains.jpg), [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/), unchanged.
- Chromium triiodide: Huang et al., [Nature 546, 270–273 (2017), Fig. 1c](https://www.nature.com/articles/nature22391/figures/1), optical micrograph, panel excerpt with scale bar retained.
- These photographs motivate the question. They are not outputs of the square-lattice simulation.

## Original course sources

- `notebooks/02_ising_model_1.ipynb`: configuration-first example and Metropolis draw order.
- `notebooks/03_ising_model_2.ipynb`: production definitions and analysis.
- `scripts/notebooks/ising_kernel.py`: unchanged kernel, copied into this package.
- `slides/06_Ising_Project_Example/build/revision5/`: guideline-aligned presentation sources.

The example has no new course-policy or grading requirements. See the current syllabus and presentation guidelines for those.
