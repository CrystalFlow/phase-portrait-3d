# High pass criteria

## What baseline ("pass") looks like

- 3D trajectories plotted for x' = Ax with a 3×3 matrix
- Eigenvector rays shown from origin
- A few example matrices demonstrated
- Clean, commented code
- Report with correct mathematical background

## What high pass requires

The professor's feedback and course context point to three levers. Hit at least two strongly.

### Lever 1 — Mathematical depth in the report

The report should go beyond restating textbook material. Strong angles:

- **Behavior types unique to 3D.** In 2D you have: stable/unstable node, saddle, center,
  spiral. In 3D you gain: a stable spiral in one eigenplane *combined with* an unstable
  real eigendirection (trajectories spiral inward but drift away); a center plane with drift
  (pure imaginary pair + nonzero real eigenvalue — trajectories orbit and translate
  simultaneously); fully 3D spirals when all three eigenvalues are complex (not possible
  in 3D with real A — worth noting why).

- **The degenerate case in 3D.** A Jordan block in one eigenplane plus a real eigenvalue
  in the third direction produces trajectories that are both polynomial-in-t and exponential.
  Draw this and explain it.

- **Eigenplanes, not just eigenvectors.** For a complex conjugate pair α ± βi, the
  "straight-line solution" generalizes to a *plane* — the real and imaginary parts of the
  eigenvector span it. Spiraling *lives* in this plane. Visualizing the plane (shaded
  surface) alongside the trajectory makes this concrete.

### Lever 2 — 4D color encoding

Color trajectories by `||x'(t)|| = ||Ax(t)||` (instantaneous speed). This choice is
mathematically justified:

- Near a stable equilibrium, speed → 0. Color shows the *rate* of convergence.
- Along an unstable eigendirection, speed grows exponentially. Color shows divergence.
- For a saddle, color reveals which part of a trajectory is "fast" vs "slow" — this
  is not visible from the 3D curve geometry alone.

Alternative 4D quantities (lower value):
- Time t — less interesting, readable from trajectory length
- Distance from origin ||x(t)|| — correlated with color but less revealing than speed

Include a colorbar and discuss what the color reveals in the report. This is the section
that most distinguishes the project from "I made a 3D plot."

### Lever 3 — Interactivity

Let the user explore rather than just observe. Specifically:

- **Matrix entry sliders** — change individual entries of A and watch trajectories update
  live. This lets you "sweep" through behavior types and observe bifurcations.
- **Initial condition picker** — click or drag to set x(0); see how different starting
  points lead to different trajectories.
- **Eigenplane toggle** — show/hide the shaded eigenplane surface to reduce visual clutter
  when needed.
- **Time range control** — extend or shorten integration to see long-term behavior vs
  short-term transients.

ipywidgets in a Jupyter notebook is the recommended approach. Plotly handles 3D rotation
natively (drag to rotate), which is itself a form of interactivity worth mentioning in
the report.

## What to discuss in the report

The strongest reports combine:
1. A moment where something *unexpected* happens visually
2. A precise mathematical explanation of *why* it happens
3. A figure that makes the explanation obvious

Good candidate moments:
- Setting the real part of the complex eigenvalue pair to exactly zero — watch the spiral
  become a closed orbit (center) in the eigenplane
- Crossing a bifurcation via a slider — a stable node suddenly becomes a saddle
- The Jordan block case: trajectory curves away from the eigenvector direction even though
  the eigenvector "should" be attracting
