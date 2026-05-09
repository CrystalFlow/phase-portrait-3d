1# Phase portrait visualizer — project context

This file gives Claude Code full context to continue development of a 3D/4D phase portrait visualizer for linear ODE systems, started in a claude.ai chat session.

## Project summary

Build an interactive Python visualizer for 3×3 linear systems **x' = Ax** that:
- Renders trajectories in true 3D
- Highlights eigenvector structure (rays from origin, eigenplanes as shaded surfaces)
- Optionally encodes a 4th dimension as color along trajectories
- Supports interactive parameter controls (matrix entries, initial conditions)

This is an **Elementary Differential Equations course project**. Deliverables are:
1. Functional, readable source code
2. A short report (3–5 single-spaced pages) with mathematical background, output figures, and discussion

Grading has two tiers: pass and **high pass**. See `docs/high_pass_criteria.md`.

## Academic context

- Course: Elementary Differential Equations
- Topic chosen: Straight-line solutions (extended to 3D/4D per professor feedback)
- Professor feedback summary: a 2D phase portrait is not high-pass worthy; a proper 3D plot with eigenvector geometry and optionally 4D color encoding is. See `docs/professor_feedback.md` for the full email.

## Architecture

Four modules, described in detail in `docs/architecture.md`:

| Module | Responsibility |
|--------|---------------|
| `solver.py` | Eigendecomposition (numpy) + trajectory integration (scipy RK45) |
| `renderer.py` | 3D plotting — trajectories, eigenvector rays, eigenplanes |
| `colormap.py` | 4D encoding — map time / speed / distance-from-origin to color |
| `controls.py` | ipywidgets sliders for live matrix entry and initial condition control |

Entry point: `main.ipynb` (Jupyter notebook — keeps code and output together for the report).

## Suggested tech stack

- Python 3.10+
- `numpy` — eigendecomposition
- `scipy` — `solve_ivp` with RK45 integrator
- `matplotlib` with `Axes3D` — static figures for the report PDF
- `plotly` — interactive 3D rotation in the notebook
- `ipywidgets` — live sliders
- `jupyter` — notebook delivery format

## Demo matrix gallery

Five matrix types to showcase in the report. See `docs/demo_matrices.md` for exact values and expected behavior.

1. **Stable node** — all eigenvalues negative real
2. **Saddle** — mixed-sign real eigenvalues
3. **Stable spiral** — complex conjugate pair (negative real part) + negative real eigenvalue
4. **Center plane + drift** — pure imaginary pair + nonzero real eigenvalue
5. **Degenerate** — repeated eigenvalue with Jordan block

## 4D encoding

Color trajectories by `||x'(t)||` (speed). This reveals:
- Trajectories *slowing* near a stable equilibrium
- Trajectories *accelerating* along unstable eigendirections

This is the mathematically meaningful 4D choice — it tells a story that equations alone cannot show.

## Report outline

1. Mathematical background — eigenvectors as straight-line solutions, extension to 3D
2. Richer behavior in 3D — behavior types not possible in 2D
3. Implementation notes — key design decisions
4. Figure gallery — one figure per demo matrix with discussion
5. 4D color encoding — what speed reveals about phase space geometry

## Current status

Project planning complete. No code written yet. Start with `solver.py`.
