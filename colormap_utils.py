"""
colormap_utils.py — Module 3: 4D color encoding for phase portrait trajectories.

Maps a scalar quantity along each trajectory to [0, 1] for colormap lookup.
Default quantity: speed = ‖x′(t)‖ = ‖Ax(t)‖ — reveals acceleration near
equilibria and along unstable eigendirections.
"""

import numpy as np


def compute_color_values(A, xyz, t, quantity='speed'):
    """
    Compute normalized color values for a single trajectory.

    Parameters
    ----------
    A        : ndarray, shape (3, 3)
    xyz      : ndarray, shape (3, N) — trajectory positions
    t        : ndarray, shape (N,)   — time points
    quantity : 'speed' | 'time' | 'distance'

    Returns
    -------
    ndarray, shape (N,), values in [0, 1]
    """
    A = np.asarray(A, dtype=float)

    if quantity == 'speed':
        # ‖Ax(t)‖ at each point — instantaneous velocity magnitude
        vel = A @ xyz          # (3, N)
        raw = np.linalg.norm(vel, axis=0)  # (N,)
    elif quantity == 'time':
        raw = t.copy()
    elif quantity == 'distance':
        raw = np.linalg.norm(xyz, axis=0)  # (N,)
    else:
        raise ValueError(f"Unknown quantity '{quantity}'. Use 'speed', 'time', or 'distance'.")

    return _normalize(raw)


def compute_color_values_many(A, trajectories, quantity='speed'):
    """
    Compute normalized color values for a list of trajectories.

    Normalization is global across all trajectories so colors are comparable.

    Parameters
    ----------
    A            : ndarray, shape (3, 3)
    trajectories : list of (t, xyz) pairs
    quantity     : 'speed' | 'time' | 'distance'

    Returns
    -------
    list of ndarray, each shape (N,), values in [0, 1]
    """
    A = np.asarray(A, dtype=float)

    raw_list = []
    for t, xyz in trajectories:
        if quantity == 'speed':
            vel = A @ xyz
            raw_list.append(np.linalg.norm(vel, axis=0))
        elif quantity == 'time':
            raw_list.append(t.copy())
        elif quantity == 'distance':
            raw_list.append(np.linalg.norm(xyz, axis=0))
        else:
            raise ValueError(f"Unknown quantity '{quantity}'.")

    # Global min/max so trajectories share the same color scale
    global_min = min(r.min() for r in raw_list)
    global_max = max(r.max() for r in raw_list)

    return [_normalize(r, global_min, global_max) for r in raw_list]


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _normalize(arr, vmin=None, vmax=None):
    vmin = arr.min() if vmin is None else vmin
    vmax = arr.max() if vmax is None else vmax
    span = vmax - vmin
    if span < 1e-15:
        return np.zeros_like(arr, dtype=float)
    return (arr - vmin) / span
