"""
demo_matrices.py — Named 3×3 matrices illustrating five qualitative behavior types.
"""

import numpy as np

MATRICES = {
    # All eigenvalues negative real. Trajectories converge to origin;
    # fastest along x₃ (λ = -3), slowest along x₁ (λ = -1).
    'stable_node': np.array([
        [-1,  0,  0],
        [ 0, -2,  0],
        [ 0,  0, -3],
    ], dtype=float),

    # Mixed-sign eigenvalues (-1, -2, +1). Stable in the x₁-x₂ plane,
    # unstable along x₃. The saddle structure is genuinely 3D.
    'saddle': np.array([
        [-1,  0,  0],
        [ 0, -2,  0],
        [ 0,  0,  1],
    ], dtype=float),

    # Eigenvalues -0.5 ± 2i and -1. Trajectories spiral inward in the
    # eigenplane of the complex pair while contracting along x₃.
    'stable_spiral': np.array([
        [-0.5, -2.0,  0.0],
        [ 2.0, -0.5,  0.0],
        [ 0.0,  0.0, -1.0],
    ], dtype=float),

    # Eigenvalues ±2i and -0.5. Pure rotation in the x₁-x₂ plane with
    # simultaneous convergence along x₃ — trajectories are helices.
    'center_drift': np.array([
        [ 0.0, -2.0,  0.0],
        [ 2.0,  0.0,  0.0],
        [ 0.0,  0.0, -0.5],
    ], dtype=float),

    # Eigenvalues -1 (multiplicity 2, Jordan block) and -2. The Jordan
    # block produces t·e^(-t) terms — trajectories curve before converging.
    'jordan': np.array([
        [-1,  1,  0],
        [ 0, -1,  0],
        [ 0,  0, -2],
    ], dtype=float),
}

# Suggested initial conditions per matrix type
INITIAL_CONDITIONS = {
    'stable_node': [
        [ 1.0,  0.0,  0.0],
        [ 0.0,  1.0,  0.0],
        [ 0.0,  0.0,  1.0],
        [ 1.0,  1.0,  1.0],
        [-1.0,  0.5, -0.5],
    ],
    'saddle': [
        [ 1.0,  0.0,  0.5],
        [ 1.0,  0.0, -0.5],
        [-1.0,  0.5,  0.3],
        [ 0.5, -1.0, -0.3],
    ],
    'stable_spiral': [
        [ 1.0,  0.0,  1.0],
        [-1.0,  0.0,  1.0],
        [ 0.0,  1.0, -1.0],
        [ 1.0,  1.0,  0.0],
    ],
    'center_drift': [
        [ 1.0,  0.0,  2.0],
        [-1.0,  0.0,  2.0],
        [ 0.0,  1.0,  2.0],
        [ 1.0,  1.0,  2.0],
    ],
    'jordan': [
        [ 1.0,  0.0,  0.0],
        [ 0.0,  1.0,  0.0],
        [ 1.0,  1.0,  1.0],
        [-1.0,  0.5,  0.5],
    ],
}

# ---------------------------------------------------------------------------
# Initial condition generators
# ---------------------------------------------------------------------------

def sphere_ics(n=16, r=1.5):
    """
    Return n points approximately evenly distributed on a sphere of radius r.

    Uses the Fibonacci lattice for near-uniform coverage — the 3D analogue
    of distributing starting points around a circle in 2D phase portraits.
    """
    ics = []
    golden = (1 + np.sqrt(5)) / 2
    for i in range(n):
        theta = np.arccos(1 - 2 * (i + 0.5) / n)
        phi = 2 * np.pi * i / golden
        ics.append([
            r * np.sin(theta) * np.cos(phi),
            r * np.sin(theta) * np.sin(phi),
            r * np.cos(theta),
        ])
    return ics


# Human-readable titles for notebook headings
TITLES = {
    'stable_node':   'Stable Node  (λ = −1, −2, −3)',
    'saddle':        'Saddle  (λ = −1, −2, +1)',
    'stable_spiral': 'Stable Spiral  (λ = −0.5 ± 2i, −1)',
    'center_drift':  'Center Plane + Drift  (λ = ±2i, −0.5)',
    'jordan':        'Degenerate / Jordan Block  (λ = −1 × 2, −2)',
}
