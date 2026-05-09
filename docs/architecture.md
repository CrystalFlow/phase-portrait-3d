# Architecture

## File structure

```
phase-portrait-3d/
├── CLAUDE.md                  # project context (this repo's root context file)
├── main.ipynb                 # entry point — notebook with all figures and controls
├── solver.py                  # Module 1: eigendecomposition + trajectory integration
├── renderer.py                # Module 2: 3D plotting
├── colormap_utils.py          # Module 3: 4D color encoding
├── controls.py                # Module 4: ipywidgets UI
├── demo_matrices.py           # convenience: named example matrices
├── report/
│   └── report.md              # written report (or .tex if LaTeX preferred)
└── docs/
    ├── professor_feedback.md
    ├── high_pass_criteria.md
    ├── architecture.md        # this file
    ├── demo_matrices.md
    └── math_background.md
```

## Module 1 — solver.py

Responsibilities:
- Accept a 3×3 numpy array A
- Return eigenvalues, eigenvectors via `numpy.linalg.eig`
- Integrate x' = Ax from a given initial condition x0 over time span [t0, tf]
  using `scipy.integrate.solve_ivp` with method='RK45'
- Return the solution as a (3, N) array of positions and (N,) array of times

Key design note: `numpy.linalg.eig` returns complex eigenvectors even when eigenvalues
are real (imaginary parts are numerical noise ~1e-16). Strip imaginary parts when
`abs(imag) < tol` for cleaner downstream handling.

For complex eigenvalue pairs, extract the real and imaginary parts of the eigenvector
separately — they span the eigenplane.

## Module 2 — renderer.py

Responsibilities:
- Create a 3D axes object (matplotlib Axes3D or plotly Figure)
- Plot trajectory curves as 3D lines, colored by the 4D quantity from colormap_utils
- Draw eigenvector rays: lines from origin to ±scale*v for each real eigenvector
- Draw eigenplanes: for each complex conjugate pair, compute the plane spanned by
  Re(v) and Im(v) and render as a shaded surface (low alpha, ~0.15)
- Accept a list of initial conditions and plot each as a separate trajectory
- Include axis labels (x₁, x₂, x₃) and a colorbar

Matplotlib vs plotly choice:
- Use matplotlib Axes3D for static report figures (savefig to PNG/PDF)
- Use plotly for the interactive notebook view (drag-to-rotate built in)
- Renderer should support both backends via a `backend='matplotlib'|'plotly'` argument

## Module 3 — colormap_utils.py

Responsibilities:
- Given a solution trajectory (positions, velocities), compute the scalar quantity
  to encode as color
- Default: speed = ||x'(t)|| = ||Ax(t)||
- Alternatives: time t, distance from origin ||x(t)||
- Return normalized values in [0, 1] for colormap lookup
- Suggested colormap: 'plasma' or 'viridis' (perceptually uniform, print-safe)

## Module 4 — controls.py

Responsibilities:
- ipywidgets FloatSlider (or BoundedFloatText) for each of the 9 matrix entries
- Widget for adding/removing initial conditions
- Toggle checkboxes: show eigenvectors, show eigenplanes, show colorbar
- Slider for integration time range [0, T]
- On any change, re-run solver + renderer and update the plot in-place

Use `ipywidgets.interactive_output` or `@interact` decorator to wire controls to the
rendering function.

## demo_matrices.py

A dictionary of named 3×3 matrices illustrating the five key behavior types.
See `docs/demo_matrices.md` for values.

## main.ipynb structure

1. Imports and setup
2. Single static figure — one matrix, one initial condition, labeled axes
3. Demo gallery — one cell per matrix type, matplotlib static figures
4. 4D color encoding demo — same matrix with and without color, side by side
5. Interactive widget — plotly + ipywidgets, full controls

The notebook IS the deliverable for the code portion of the project.
