---
title: "Agent Skills: Research Intel Agent (RIA)"
date: 2026-05-05
author:
  name: "Young Woo Choi"
  email: "ywchoi02@sogang.ac.kr"
tags: ["claude-code-skill", "literature-scan", "openalex", "arxiv", "research-agent"]
---

> ⚠️ This note is meant to publish agent skills actually being used in our lab, but the present draft was written by Claude. It has not yet been reviewed by Y.W. Choi. Treat the description and excerpts as agent-generated until that review happens.

A Claude Code skill that scans the literature once per day and posts research-gap candidates to a Slack channel with strict inline citations. Lives at `~/julia/base/skills/research-intel/` and runs nightly via cron at 21:00 KST.

## Core idea

The skill is built around one rule: *every factual claim about existing work must point to a specific paper*. That single constraint makes the agent useful as a suggestion tool — it cannot hand-wave a gap into existence, because every sentence has to terminate in an `[N]` marker that matches an entry in a `References` block with a real DOI or arXiv ID.

On top of that, three layers shape what gets sent.

**Layer 1 — collect.** A small Python tool (`tools/collect.py`) pulls candidates from four sources in parallel: a local feeds DB (filtered by score and recency), the OpenAlex API for a curated list of "key people" (Louie / Qiu / Z. Li / da Jornada / C.-H. Park / Cao / Naik / Giustino / Poncé / Margine / ... — roughly 17 PIs across GW-BSE, electron-phonon, moiré, and code developers), arXiv's `cond-mat.*` Atom feeds, and on-demand topic searches once a pattern starts to emerge.

**Layer 2 — verify the gap.** For each candidate idea, the agent searches for at least three adjacent papers (by topic and by citing-works lookup on a key DOI) before keeping it. Anything already filled by an existing study, or so obvious it appears in every review, gets discarded. Four idea archetypes are allowed: `gap` (a calculation that should exist but doesn't), `anomaly` (data that doesn't match theory), `surprise` (an unexpected result nobody followed up), `unlock` (a new method that makes a previously infeasible calculation tractable).

**Layer 3 — timeliness.** Each surviving idea gets a `High`/`Medium`/`Low` confidence flag based on whether there are active publications, fresh experimental data, a newly released code, or upcoming conference sessions on the topic.

The output is at most three ideas per day, sent first as a Korean+English mixed message to a dedicated Slack channel and then mirrored as an English-only thread reply. Each idea is structured into three blocks — *Missing* (what's been done, where it stops, and what's specifically absent), *Why now* (the timeliness evidence), *Risks* (what could make the calculation fail or be uninformative) — followed by a numbered `References` list. A self-check pass before sending verifies that every `[N]` in the body resolves, every reference is cited at least once, and every reference has a working link. Each daily run is also archived as a markdown file under `reports/YYYY-MM-DD.md`.

A `state/feedback.json` file accumulates PI responses so the agent can recalibrate over time: directions marked *interested* get pursued harder; *rejected: already done* triggers more thorough verification on the next attempt; *rejected: not interesting* removes that topic-pattern combination from future scans.

## Example intel — abridged

The excerpts below are from real daily runs. They illustrate the message structure rather than the full content; full reports live in `reports/` inside the skill directory.

### Example 1 — `unlock`, High confidence (2026-05-04)

> 💡 **Idea 1: Photoexcited exciton populations dynamically reshape the moiré potential — light-driven reorganisation of Wigner-crystal / FCI / vHS-AHE phase boundaries.** `unlock` · confidence `High`
>
> *Missing:* Del Grande & Strubbe explain the microscopic origin of the *0.1 Å light-induced interlayer-distance change* in 1.1° tWSe2 via a multi-scale GW-BSE+DFPT framework [1] — but the coupling is single-shot: *exciton population → equilibrium displacement*. Concurrently, You et al. (Louie/Cao/Naik) establish *moiré excitons inside a generalized Wigner crystal* ab initio [2], and Ke et al. demonstrate via a DeePMD+DeepH ML workflow that *dynamic moiré potentials produce robust Wigner crystallisation* in large-scale twisted TMDs [3]. (...) A first-principles study of the *self-consistent feedback* from photo-excited exciton population → moiré potential modulation → Wigner-crystal stability / FCI plateau / vHS-AHE hot-spot location is missing.
>
> *Why now:* (a) Del Grande [1] (2026-04-30) makes the exciton-phonon multi-scale framework production-ready; (b) You et al. PNAS [2] supplies the equilibrium Wigner-crystal baseline; (c) Ke et al. [3] makes large-supercell time evolution feasible; (d) yesterday's RIA Idea 2 reports a spontaneous AHE hot spot at 4.8° tMoTe2 [7] — a falsifiable target via a light-induced hot-spot sweep.
>
> ⚠️ *Risks:* the exciton-phonon-structure self-consistent loop is BSE↔relaxation iterative and costly. Practical first case: evaluate the breathing-mode amplitude of 1.1° tWSe2 self-consistently as a function of exciton density, then propagate to the 4.8° tMoTe2 vHS regime.
>
> 📎 *References*
> [1] R. R. Del Grande and D. A. Strubbe, *arXiv:2604.28143* (2026).
> [2] J.-Y. You et al., *Proc. Natl. Acad. Sci.* (2026), DOI:10.1073/pnas.2531259123.
> [3] Y. Ke et al., *arXiv:2604.22343* (2026).
> [7] H. Park et al., *arXiv:2604.23587* (2026).

### Example 2 — `anomaly`, hypothesis update (2026-05-03)

> 💡 **Idea 3: 1T-TiSe2 bulk *T\* ≈ 165 K* (ultrafast) coincides with surface *T_SRS ≈ 160 K* (micro-ARPES) — *bulk EP-driven hidden lattice instability* framing (yesterday's surface-excitonic hypothesis updated).** `anomaly` · confidence `High`
>
> *Missing:* Yesterday's RIA Idea 1 interpreted the Yilmaz et al. micro-ARPES *surface SRS collapse at 160 K* [1] through a *surface excitonic* channel. Today's new evidence: Ye et al. v2 [2] reports a bulk ultrafast pump-probe characteristic temperature *T\* ≈ 165 K* — A_{1g}-mode lattice-potential stiffening with metastable-state formation. The 5 K coincidence is hard to dismiss, so yesterday's surface-only framing should be updated. Missing: anharmonic free energy across T = 50–300 K, EP-driven polaron self-trapping comparison between bulk and surface, non-equilibrium reproduction of the metastable state.
>
> *Why now:* (a) Ye v2 [2] (2026-04-28) supplies a quantitative bulk T\* target; (b) yesterday's surface-only framing is now challenged by the 5 K coincidence; (c) the Lihm-Park CH non-perturbative EP framework is transferable to anharmonic + self-trapping analysis.
>
> ⚠️ *Risks:* anharmonic free-energy calculations (TDEP/SCAILD) need large supercells and multi-T sampling — costly. First case: bulk 1T-TiSe2 at T = 100, 165, 200 K — anharmonic free energy + soft-mode amplitude — to decide whether a hidden 165 K instability exists at all.

This second example illustrates one habit of the agent that turns out to be useful: it explicitly flags when *yesterday's* framing has been overtaken by today's evidence and writes the update into the *Missing* block, rather than silently producing a contradictory new idea.

### Example 3 — pure `gap` (2026-04-30)

> 💡 **Idea 1: TMD/hBN remote Fröhlich coupling — replace the modified-Fröhlich model with full ab initio supercell DFPT + Wannier interpolation.** `gap` · confidence `High`
>
> *Missing:* Gatti et al. [1] observed, by ARPES on monolayer TMD/hBN stacks, that hBN polar phonons remotely dress TMD quasiparticles and produce *replica bands* — but the theory side stops at a *modified Fröhlich model* with only "semi-quantitative agreement". Sohier-Calandra-Mauri's 2D Fröhlich first-principles framework [2] handles only *isolated* monolayer TMDs, with no remote substrate phonon. Existing substrate-remote-phonon work [3] is at the tight-binding effective-Fröhlich level. The full *TMD/hBN heterostructure supercell DFPT + Wannier-interpolated cross-interface remote Fröhlich coupling g_νk(q)* is therefore missing.

