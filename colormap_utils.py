"""
colormap_utils.py — Module 3: 4D color encoding for phase portrait trajectories.

Maps a scalar quantity along each trajectory to [0, 1] for colormap lookup.
Default quantity: speed = ‖x′(t)‖ = ‖Ax(t)‖ — reveals acceleration near
equilibria and along unstable eigendirections.
"""

import numpy as np


def _compute_raw(A, xyz, t, quantity):
    """
    Parameters
    ----------
    A        : ndarray (3, 3)
    xyz      : ndarray (3, N) — trajectory positions
    t        : ndarray (N,)   — time points
    quantity : 'speed' | 'time' | 'distance'

    Returns
    -------
    ndarray (N,), unnormalized scalar values
    """
    if quantity == 'speed':
        return np.linalg.norm(A @ xyz, axis=0)
    elif quantity == 'time':
        return t
    elif quantity == 'distance':
        return np.linalg.norm(xyz, axis=0)
    else:
        raise ValueError(f"Unknown quantity '{quantity}'. Use 'speed', 'time', or 'distance'.")


def compute_color_values(A, xyz, t, quantity='speed'):
    """
    Compute normalized color values for a single trajectory (local normalization).

    Note: normalization is per-trajectory; results are not comparable across
    multiple trajectories. Use compute_color_values_many for global normalization.

    Returns
    -------
    ndarray (N,), values in [0, 1]
    """
    return _normalize(_compute_raw(np.asarray(A, dtype=float), xyz, t, quantity))


def compute_color_values_many(A, trajectories, quantity='speed'):
    """
    Compute normalized color values for a list of trajectories.

    Normalization is global across all trajectories so colors are comparable.

    Parameters
    ----------
    A            : ndarray (3, 3)
    trajectories : list of (t, xyz) pairs — one per initial condition
    quantity     : 'speed' | 'time' | 'distance'

    Returns
    -------
    list of ndarray, each shape (N,), values in [0, 1]
    """
    A = np.asarray(A, dtype=float)
    raw_list = [_compute_raw(A, xyz, t, quantity) for t, xyz in trajectories]
    all_raw = np.concatenate(raw_list)
    global_min, global_max = all_raw.min(), all_raw.max()
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
