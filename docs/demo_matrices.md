# Demo matrices

Five matrices covering the key qualitative behavior types for 3×3 linear systems.
Each entry includes the matrix, its eigenvalues, and what to observe in the plot.

---

## 1. Stable node

All eigenvalues negative real. All trajectories converge to origin along eigenvector directions.

```python
A = np.array([
    [-1,  0,  0],
    [ 0, -2,  0],
    [ 0,  0, -3]
])
```

Eigenvalues: -1, -2, -3 (diagonal, so eigenvectors are e₁, e₂, e₃)

What to observe:
- All trajectories flow toward origin
- Trajectories are fastest along the x₃ direction (eigenvalue -3), slowest along x₁
- Color (speed) is brightest far from origin, dims as trajectories converge
- Use multiple initial conditions spread across the unit sphere

---

## 2. Saddle (mixed signs)

One positive, two negative eigenvalues. Unstable along one eigenvector, stable in the eigenplane of the other two.

```python
A = np.array([
    [-1,  0,  0],
    [ 0, -2,  0],
    [ 0,  0,  1]
])
```

Eigenvalues: -1, -2, +1

What to observe:
- Trajectories approach the x₁-x₂ plane (stable eigenplane) but are repelled along x₃
- The "saddle" structure is genuinely 3D here — in 2D you can only show a 2D saddle
- Color reveals the acceleration along the unstable direction
- Initial conditions both above and below the stable plane show the separation clearly

---

## 3. Stable spiral (complex pair + real)

A complex conjugate pair with negative real part (spiraling inward in eigenplane)
plus a negative real eigenvalue (converging in the third direction).

```python
A = np.array([
    [-0.5, -2,   0],
    [ 2,   -0.5, 0],
    [ 0,    0,  -1]
])
```

Eigenvalues: -0.5 ± 2i, -1

What to observe:
- Trajectories spiral in the x₁-x₂ plane (eigenplane of the complex pair)
- Simultaneously contract along x₃
- The eigenplane (x₁-x₂ plane here, since block-diagonal) should be shown as a shaded surface
- This behavior type does not exist in 2D systems — a key point for the report
- Color shows speed oscillating as the spiral rotates (faster at larger radius)

---

## 4. Center plane + drift

Pure imaginary eigenvalue pair (orbiting in eigenplane, no decay) plus a nonzero real eigenvalue (drift in third direction). Trajectories are helices.

```python
A = np.array([
    [ 0, -2,  0],
    [ 2,  0,  0],
    [ 0,  0, -0.5]
])
```

Eigenvalues: ±2i, -0.5

What to observe:
- Trajectories orbit in the x₁-x₂ plane (center) while converging along x₃
- Result: a downward (or upward) helix — visually striking
- Change the (3,3) entry from -0.5 to +0.5 to get an expanding helix
- Pure imaginary eigenvalues: the orbit neither grows nor decays in the eigenplane
- This is a case where the 3D figure tells you something the eigenvalues alone don't
  make immediately obvious

---

## 5. Degenerate (repeated eigenvalue, Jordan block)

A repeated eigenvalue with a Jordan block — the algebraic multiplicity exceeds the geometric multiplicity. Solutions involve polynomial × exponential terms.

```python
A = np.array([
    [-1,  1,  0],
    [ 0, -1,  0],
    [ 0,  0, -2]
])
```

Eigenvalues: -1 (multiplicity 2, one eigenvector), -2

What to observe:
- In the x₁-x₂ subspace: the Jordan block produces solutions like t·e^(-t)
  — trajectories initially move *away* from the eigenvector direction before converging
- Along x₃: standard exponential decay
- The "kink" in trajectories near the eigenvector direction is the key visual
- This is a case where drawing the straight-line solution alone (just the eigenvector)
  is deeply misleading — the Jordan block changes the geometry significantly
- Worth a dedicated discussion in the report

---

## Usage in code

```python
from demo_matrices import MATRICES

# MATRICES is a dict:
# {
#   'stable_node': np.array(...),
#   'saddle': np.array(...),
#   'stable_spiral': np.array(...),
#   'center_drift': np.array(...),
#   'jordan': np.array(...),
# }
```
