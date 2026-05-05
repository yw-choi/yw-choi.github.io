---
title: "Crystal structure 4-view plot"
date: 2026-05-05
tags: ["python", "ase", "matplotlib", "visualization", "claude-code-skill"]
summary: "A Claude Code Agent Skill that renders publication-quality 4-view crystal-structure figures (view ‖ a, view ‖ b, view ‖ c, perspective) directly from a CIF/POSCAR/XYZ file or an ASE preset — no GUI."
---

Every time I make a crystal-structure figure for a paper or talk, I open VESTA, rotate the model, tweak export settings, and re-run the same dance. To remove that loop I built a small renderer that takes one ASE-readable input and writes a 2×2 PNG with the four standard views. The defaults were calibrated against eight published Nature / PRX / Sci. Adv. structure figures and tightened over ~10 review iterations.

The script ships as a Claude Code Agent Skill so I can also invoke it conversationally ("plot MoS2 monolayer"), but it is just a Python file — `python plot_crystal.py mx2:MoS2 -o mos2.png` works on its own.

![MoS2 monolayer 4-view](thumbnail.png)

## What it draws

| panel | view |
|---|---|
| **a** | view ‖ a (camera along the a-axis, screen = bc plane) |
| **b** | view ‖ b |
| **c** | view ‖ c (top view) |
| **d** | perspective (a ←, b →, c ↑) |

The perspective rotation is composed as `R = Rx(α) @ Rz(β)`. Because `Rz` rotates around c first, **the c-axis is always exactly vertical on screen** for any tilt α. The default `(α = -55°, β = 210°)` puts the a-axis down-left and the b-axis down-right symmetrically, with c straight up.

## Usage

Once installed under `~/.claude/skills/crystal-plot/`:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/plot_crystal.py" mx2:MoS2 -o mos2.png
```

Or run the script directly from a clone of the repo:

```bash
python3 scripts/plot_crystal.py mx2:MoS2 -o mos2.png
```

Input can be:

- a structure file (`.cif`, `POSCAR`, `.vasp`, `.xyz`, `.traj` — anything `ase.io.read` accepts)
- an ASE preset: `mx2:MoS2`, `mx2:WSe2:1T`, `bulk:Si`, `bulk:NaCl:rocksalt:5.64`, `graphene`

## Common options

```text
--repeat NX,NY,NZ       supercell repeat (default: 3,3,1 if layered, else 2,2,2)
--perspective AX,AZ     tilt + azimuth in degrees (default: -55,210)
--bond-scale 1.15       bond cutoff = scale × Σr_cov
--radius-scale 0.40     atom radius = covalent_radius × scale
--no-cell-box           omit the dashed cell box on the perspective panel
--dpi 240
--figsize 11,8
```

## More examples

```bash
python3 scripts/plot_crystal.py bulk:Si -o si.png
```

![Diamond Si](example_si.png)

```bash
python3 scripts/plot_crystal.py bulk:NaCl:rocksalt:5.64 -o nacl.png
```

![NaCl rocksalt](example_nacl.png)

## Conventions baked in

The defaults are not opinions — they are the contract. Calibrated through review against published figures.

- **Atoms** rendered as Phong-shaded sphere images (ambient 0.32 + diffuse 0.70, light from the upper-left at `(-0.45, 0.55, 0.70)`), 1-pixel anti-aliased rim, no specular highlight. Cached by color, so a 1000-atom figure still renders quickly.
- **Bonds** are two-tone, split at the midpoint, no dark outline, width ≈ 0.11 × bond length. The cutoff is `scale × Σr_cov` (default 1.15) with two refinements:
  - reject same-element bonds when covalent radius > 1.30 Å (kills incidental Mo-Mo, W-W in layered crystals)
  - reject long heavy-metal bonds where `d > Σr_cov`
  - both rules check covalent radius > 1.30 Å so Si, C, and other genuinely covalent solids stay bonded.
- **Palette**: a softened VESTA-Jmol scheme (Mo = teal, S = mustard, O = red, …).
- **Depth (perspective only)**: front atoms full size, back atoms 0.78×, linear in projected depth. Per-atom `zorder` so closer spheres occlude farther ones; bond width and `zorder` scale together.
- **Tripod**: a / b / c arrows in RGB (red / green / blue) with italic lowercase labels and a white halo. The axis pointing into the screen is shown as a small white circle with a center dot. Each panel reserves a structure-free margin in the chosen corner so the arrows never overlap atoms.
- **Cell box**: dashed blue (`#0d33bf`, 4-on / 3-off, 0.7 pt), drawn only on the perspective panel by default.
- **Not included**: "view ‖ a" text labels (rejected during review), specular highlights, depth fog, ground-plane shadows.

## Dependencies

```text
numpy, matplotlib, ase
```

ASE is the only one not in a typical conda base. `pip install --user ase` is enough; the script exits cleanly with code 2 if any dependency is missing.

## Code

[`sogang-qmp/skills-crystal-plot`](https://github.com/sogang-qmp/skills-crystal-plot) — public, MIT. Single-file renderer, ~470 LoC.

## Out of scope

- Interactive 3D viewer — use `ase gui` or VESTA.
- Polyhedral rendering (perovskite octahedra, ZIF tetrahedra) — ball-and-stick only.
- Charge density / orbital isosurfaces — VESTA + `.cube` is still the right tool.
