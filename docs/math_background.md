# Mathematical background

Reference material for the report's background section.
This should be written in your own words; this doc is a structured outline, not prose to copy.

---

## 1. Straight-line solutions (the 2D foundation)

For x' = Ax with x ∈ ℝ², if Av = λv (v is an eigenvector, λ is the eigenvalue), then:

    x(t) = c · e^(λt) · v

is a solution for any scalar c. This is a "straight-line solution" because x(t) always
points in the direction of v — it only scales, never rotates.

The general solution (when A has two independent eigenvectors v₁, v₂) is:

    x(t) = c₁ e^(λ₁t) v₁ + c₂ e^(λ₂t) v₂

The phase portrait is determined by the signs and nature of λ₁, λ₂.

---

## 2. Extension to 3D

For x ∈ ℝ³, the same principle applies. With three independent eigenvectors:

    x(t) = c₁ e^(λ₁t) v₁ + c₂ e^(λ₂t) v₂ + c₃ e^(λ₃t) v₃

The straight-line solutions are rays along each eigenvector vᵢ.

New behavior types (not present in 2D):
- A spiral *in a plane* combined with exponential growth/decay *perpendicular to that plane*
- Helical trajectories (center in eigenplane + drift in normal direction)
- Saddles with a 2D stable manifold and 1D unstable manifold (or vice versa)

---

## 3. Complex eigenvalues in 3D

Real 3×3 matrices always have at least one real eigenvalue (characteristic polynomial
degree 3, always has a real root). The other two are either both real or a complex
conjugate pair α ± βi.

For a complex conjugate pair with eigenvector w = u + iv (u, v ∈ ℝ³):

The corresponding solutions are:

    x(t) = e^(αt) [c₁(cos(βt)u − sin(βt)v) + c₂(sin(βt)u + cos(βt)v)]

This is motion in the **eigenplane** span{u, v}, with:
- Exponential scaling at rate α (decaying if α < 0, growing if α > 0, orbiting if α = 0)
- Rotation at rate β within the plane

The eigenplane is the natural generalization of the "straight-line solution" for complex
eigenvalues — the orbit lives in a 2D plane in 3D space.

---

## 4. The Jordan block case

When a 3×3 matrix has a repeated eigenvalue λ with only one linearly independent
eigenvector (defective matrix), the general solution involves polynomial terms:

    x(t) = e^(λt) [c₁v + c₂(tv + w)]

where w is a generalized eigenvector satisfying (A − λI)w = v.

This means solutions grow polynomially in t (modified by the exponential). The
trajectory near the eigenvector direction "curves away" before converging — producing
the characteristic kink visible in the 3D phase portrait.

---

## 5. The 4D color encoding — mathematical justification

Coloring by speed ||x'(t)|| = ||Ax(t)|| is meaningful because:

- ||x'(t)|| = 0 only at the equilibrium x = 0 (for invertible A)
- Along a solution x(t) = e^(λt)v (real eigenvalue λ, eigenvector v):
    ||x'(t)|| = |λ| · |c| · e^(λt) · ||v||
  → speed decays exponentially for stable directions, grows for unstable ones

- The ratio of speeds in different eigendirections equals the ratio |λ₁|/|λ₂|
  — color directly encodes relative eigenvalue magnitude along each trajectory

This turns the colormap into a quantitative tool, not just decoration.

---

## 6. Key result to state in the report

The straight-line solutions (eigenvector rays) form the *skeleton* of the phase portrait.
Every trajectory is a linear combination of the straight-line (and spiraling) solutions.
Understanding the eigenvectors and eigenvalues completely determines the qualitative
behavior — but *seeing* this in 3D, particularly for complex eigenvalues and degenerate
cases, requires visualization that 2D cannot provide.
