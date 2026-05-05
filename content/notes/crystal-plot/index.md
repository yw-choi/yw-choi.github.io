---
title: "Agent Skills: crystal structure plot"
date: 2026-05-05
tags: ["python", "ase", "matplotlib", "visualization", "claude-code-skill"]
---

## How to use

```bash
python3 scripts/plot_crystal.py <input> -o out.png
```

`<input>` is a structure file (`.cif`, `POSCAR`, `.vasp`, `.xyz`, `.traj`) or a preset (`mx2:MoS2`, `bulk:Si`, `graphene`).

## Example outputs

![MoS2 monolayer](thumbnail.png)

![Diamond Si](example_si.png)

![NaCl rocksalt](example_nacl.png)

## Repo

[sogang-qmp/skills-crystal-plot](https://github.com/sogang-qmp/skills-crystal-plot)
