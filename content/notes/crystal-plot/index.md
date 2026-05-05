---
title: "Agent Skills: crystal structure plot"
date: 2026-05-05
tags: ["python", "ase", "matplotlib", "visualization", "claude-code-skill"]
---

A simple Claude Code agent skill for crystal-structure plotting — a reasonable starting point for further tuning.

## How to use

Install once:

```bash
git clone https://github.com/sogang-qmp/skills-crystal-plot.git \
    ~/.claude/skills/crystal-plot
```

Then ask the agent in natural language. The skill triggers on phrases like *plot the structure of MoS2 monolayer*, *render this POSCAR*, *VESTA-like figure of bulk Si*, or the Korean equivalents (결정구조 플롯, 원자구조 그려, …). The agent picks up the input — a structure file you supplied (`.cif`, `POSCAR`, `.vasp`, `.xyz`, `.traj`) or a preset like `mx2:MoS2`, `bulk:Si`, `graphene` — runs the renderer, and returns a PNG.

Defaults (perspective angle, bond cutoff, color palette, depth scaling) are calibrated against published Nature / PRX figures. Override any of them via natural language, e.g. *use a steeper tilt, no cell box, repeat 4×4×1*.

## Example outputs

![MoS2 monolayer](thumbnail.png)

![Diamond Si](example_si.png)

![NaCl rocksalt](example_nacl.png)

## Repo

[sogang-qmp/skills-crystal-plot](https://github.com/sogang-qmp/skills-crystal-plot)
