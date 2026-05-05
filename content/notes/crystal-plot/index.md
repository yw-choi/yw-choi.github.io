---
title: "Crystal structure 4-view plot"
date: 2026-05-05
tags: ["python", "ase", "matplotlib", "visualization", "claude-code-skill"]
summary: "Publication-quality VESTA-like 4-view crystal structure figure (view ‖ a, view ‖ b, view ‖ c, perspective) — ASE 입력 + matplotlib 렌더러로 외부 GUI 없이 PNG 한 장 생성."
---

VESTA로 결정구조 figure를 그릴 때마다 GUI를 열고 회전시키고 export 설정을 맞추는 게 반복적이라서, ASE 입력 한 줄로 4-view 패널을 PNG로 뽑아내는 스크립트를 만들었습니다. Nature / PRX / Sci. Adv. 의 결정구조 figure 8편을 비교하며 컨벤션을 칼리브레이션 했고, 사용자 검토 ~10회를 거쳐 기본값을 고정했습니다.

![MoS2 4-view](thumbnail.png)

## 무엇을 그리는가

한 figure에 네 패널:

| 패널 | 시점 |
|---|---|
| **a** | view ‖ a (a축 방향에서 본 모습, 화면 = bc 평면) |
| **b** | view ‖ b |
| **c** | view ‖ c (top view) |
| **d** | perspective (a ←, b →, c ↑) |

Perspective는 회전 행렬을 `R = Rx(α) @ Rz(β)` 순서로 구성해서 어떤 tilt 각에서도 **c축이 화면에서 정확히 수직**으로 유지되도록 했습니다. 기본값 `α=-55°, β=210°`이면 a/b가 좌하·우하로 대칭, c가 위쪽.

## 사용법

```bash
# Claude Code skill로 호출
python3 ~/julia/base/skills/crystal-plot/scripts/plot_crystal.py mx2:MoS2 -o mos2.png
```

또는 sogang-qmp/skills 로 symlink 했다면:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/plot_crystal.py" mx2:MoS2 -o mos2.png
```

입력은 다음 중 하나:

- 구조 파일 (`.cif`, `POSCAR`, `.vasp`, `.xyz`, `.traj` 등 ASE가 읽을 수 있는 모든 포맷)
- ASE preset: `mx2:MoS2`, `mx2:WSe2:1T`, `bulk:Si`, `bulk:NaCl:rocksalt:5.64`, `graphene`

## 주요 옵션

```text
--repeat NX,NY,NZ       supercell 반복 (default: 3,3,1 if layered, else 2,2,2)
--perspective AX,AZ     기본 -55,210
--bond-scale 1.15       bond 컷오프 = scale × Σr_cov
--radius-scale 0.40     atom 반지름 = covalent_radius × scale
--no-cell-box           perspective 패널의 dashed cell box 끄기
--dpi 240
```

## 다른 결정 예시

```bash
python3 plot_crystal.py bulk:Si -o si.png
```

![Diamond Si](example_si.png)

```bash
python3 plot_crystal.py bulk:NaCl:rocksalt:5.64 -o nacl.png
```

![NaCl rocksalt](example_nacl.png)

## 렌더링 컨벤션

VESTA를 쓰면서 항상 손으로 만지던 부분을 모두 기본값으로 고정했습니다:

- **Atom**: pixel-level Phong shading (ambient 0.32 + diffuse 0.70, 광원 좌상단 (-0.45, 0.55, 0.70)). 1픽셀 anti-aliased rim. specular 없는 matte. 같은 색의 sphere는 캐싱돼서 1000개 atom도 빠르게 렌더.
- **Bond**: two-tone (중간점에서 색 split), dark outline 없음, 두께 ≈ 0.11 × bond length.
- **Bond cutoff**: 1.15 × Σ(공유결합반지름). 추가 규칙으로 같은 원소 + cov_radius > 1.30 Å (Mo-Mo, W-W 등) 제외, heavy-metal m-m + d > Σr_cov 제외. 이 규칙이 covalent solid (Si, C 등)에는 영향 없도록 cov_radius > 1.30 조건을 같이 걸었음.
- **Palette**: VESTA-Jmol을 약 20% desaturate한 톤 (Mo = teal, S = mustard, O = red).
- **Depth (perspective)**: 가까운 atom 100% / 먼 atom 78% 크기로 선형 스케일. per-atom zorder로 occlude. bond 두께·zorder도 동시 스케일.
- **Tripod**: a/b/c 화살표 RGB(red/green/blue), italic lowercase 라벨에 흰 halo. 화면 평면을 뚫고 들어가는 축은 흰 동그라미 + 가운데 점.
- **Cell box**: dashed 파란선 (0.7 pt), perspective 패널에만.
- **No** "view ‖ a/b/c" 텍스트 라벨, **no** specular highlight, **no** depth fog, **no** shadow.

## 의존성

```text
numpy, matplotlib, ase
```

ASE가 conda base에 없을 수 있어서 `pip install --user ase` 한번 필요.

## 코드

- 개인 julia: [`yw-choi/julia` /base/skills/crystal-plot](https://github.com/yw-choi/julia/tree/main/base/skills/crystal-plot)
- 연구실 공용: [`sogang-qmp/skills` /crystal-plot](https://github.com/sogang-qmp/skills/tree/main/crystal-plot)

스크립트는 단일 파일 (~470 LoC) 이고 numpy + matplotlib + ase만 의존하니, Claude Code 환경 밖에서도 그대로 실행 가능합니다.

## 한계

- ball-and-stick 전용. 다면체 (perovskite octahedra, ZIF tetrahedra) 렌더링 안 함.
- 인터랙티브 viewer 아님 — 결과는 정적 PNG. 회전/줌이 필요하면 `ase gui` 또는 VESTA.
- charge density / orbital isosurface 미지원.
