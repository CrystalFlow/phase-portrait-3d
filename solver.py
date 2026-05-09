"""
solver.py — Module 1: eigendecomposition and trajectory integration for x' = Ax.
"""

import numpy as np
from scipy.integrate import solve_ivp


# ---------------------------------------------------------------------------
# Eigendecomposition
# ---------------------------------------------------------------------------

def analyze(A, tol=1e-10):
    """
    Compute eigenvalues and eigenvectors of a 3×3 matrix A.

    Returns
    -------
    eigenvalues : ndarray, shape (3,), dtype complex
    eigenvectors : list of dicts, length 3
        Each dict has keys:
            'value'  : complex eigenvalue
            'vector' : ndarray — real vector (shape (3,)) for real eigenvalues,
                       or tuple (Re(v), Im(v)) of real arrays for complex ones
            'type'   : 'real' | 'complex'
        Complex conjugate pairs appear consecutively; only the first of the pair
        is returned (the conjugate carries no new geometric information).
    """
    A = np.asarray(A, dtype=float)
    if A.shape != (3, 3):
        raise ValueError("A must be a 3×3 matrix.")

    vals, vecs = np.linalg.eig(A)

    result = []
    skip = set()
    for i in range(3):
        if i in skip:
            continue
        lam = vals[i]
        v = vecs[:, i]

        if abs(lam.imag) < tol:
            # Real eigenvalue — strip negligible imaginary noise
            result.append({
                'value': lam.real,
                'vector': v.real.copy(),
                'type': 'real',
            })
        else:
            # Complex eigenvalue — find conjugate partner
            re_v = v.real.copy()
            im_v = v.imag.copy()
            result.append({
                'value': lam,
                'vector': (re_v, im_v),
                'type': 'complex',
            })
            # Mark conjugate as handled
            for j in range(i + 1, 3):
                if j not in skip and abs(vals[j] - lam.conjugate()) < tol:
                    skip.add(j)
                    break

    return vals, result


# ---------------------------------------------------------------------------
# Trajectory integration
# ---------------------------------------------------------------------------

def integrate(A, x0, t_span=(0, 10), n_points=500):
    """
    Integrate x' = Ax from initial condition x0 over t_span.

    Parameters
    ----------
    A        : array-like, shape (3, 3)
    x0       : array-like, shape (3,)
    t_span   : (t0, tf)
    n_points : number of output time points

    Returns
    -------
    t    : ndarray, shape (N,)
    xyz  : ndarray, shape (3, N)  — trajectory positions
    """
    A = np.asarray(A, dtype=float)
    x0 = np.asarray(x0, dtype=float)

    def ode(t, x):
        return A @ x

    t_eval = np.linspace(t_span[0], t_span[1], n_points)
    sol = solve_ivp(ode, t_span, x0, method='RK45', t_eval=t_eval,
                    rtol=1e-8, atol=1e-10, dense_output=False)

    if not sol.success:
        raise RuntimeError(f"Integration failed: {sol.message}")

    return sol.t, sol.y  # sol.y has shape (3, N)


def integrate_many(A, x0_list, t_span=(0, 10), n_points=500):
    """
    Integrate multiple initial conditions. Returns a list of (t, xyz) pairs.
    """
    return [integrate(A, x0, t_span, n_points) for x0 in x0_list]
