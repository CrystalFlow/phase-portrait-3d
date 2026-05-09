"""
renderer.py — Module 2: 3D plotting of trajectories, eigenvector rays, and eigenplanes.

Uses Plotly for interactive 3D rotation in the notebook.
"""

import numpy as np
import plotly.graph_objects as go


# Matplotlib colormap names → Plotly colorscale names
_COLORSCALE_MAP = {
    'plasma': 'plasma', 'viridis': 'viridis',
    'inferno': 'inferno', 'magma': 'magma',
    'cividis': 'cividis',
}


def plot_phase_portrait(
    trajectories,
    eigen_info=None,
    color_values=None,
    colormap='plasma',
    eigvec_scale=3.0,
    eigenplane_scale=3.0,
    show_eigenvectors=True,
    show_eigenplanes=True,
    show_colorbar=True,
    title=None,
):
    """
    Render an interactive 3D phase portrait with Plotly.

    Parameters
    ----------
    trajectories : list of (t, xyz) pairs
        Each xyz has shape (3, N).
    eigen_info : list of dicts from solver.analyze(), or None
        If provided, draws eigenvector rays and eigenplanes.
    color_values : list of 1-D arrays or None
        One array per trajectory (same length as trajectory time points),
        pre-normalized to [0, 1] by colormap_utils.
        If None, trajectories are plotted in a single default color.
    colormap : str
        Colormap name — 'plasma', 'viridis', 'inferno', 'magma', or 'cividis'.
    eigvec_scale : float
        Length of eigenvector ray in each direction from the origin.
    eigenplane_scale : float
        Half-width of the eigenplane grid.
    show_eigenvectors : bool
    show_eigenplanes : bool
    show_colorbar : bool
    title : str or None

    Returns
    -------
    plotly.graph_objects.Figure
    """
    colorscale = _COLORSCALE_MAP.get(colormap, 'plasma')
    traces = []

    # --- Trajectories ---
    for idx, (t, xyz) in enumerate(trajectories):
        cv = color_values[idx] if color_values is not None else None

        if cv is not None:
            colorbar_cfg = dict(
                title='‖x′(t)‖<br>(normalized)',
                thickness=15,
                len=0.6,
            ) if (idx == 0 and show_colorbar) else None

            traces.append(go.Scatter3d(
                x=xyz[0], y=xyz[1], z=xyz[2],
                mode='lines',
                line=dict(
                    color=cv,
                    colorscale=colorscale,
                    width=3,
                    cmin=0, cmax=1,
                    colorbar=colorbar_cfg,
                ),
                showlegend=False,
            ))
        else:
            traces.append(go.Scatter3d(
                x=xyz[0], y=xyz[1], z=xyz[2],
                mode='lines',
                line=dict(width=3),
                showlegend=False,
            ))

        # Mark initial condition
        traces.append(go.Scatter3d(
            x=[xyz[0, 0]], y=[xyz[1, 0]], z=[xyz[2, 0]],
            mode='markers',
            marker=dict(size=4, color='black'),
            showlegend=False,
        ))

    # --- Eigenplanes (drawn first so rays appear on top) ---
    if eigen_info is not None and show_eigenplanes:
        for eig in eigen_info:
            if eig['type'] == 'complex':
                traces.extend(_eigenplane_traces(eig['vector'], eigenplane_scale))

    # --- Eigenvector rays ---
    if eigen_info is not None and show_eigenvectors:
        for eig in eigen_info:
            if eig['type'] == 'real':
                traces.extend(_eigenvector_traces(eig['vector'], eigvec_scale))

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            title=title,
            scene=dict(
                xaxis_title='x₁',
                yaxis_title='x₂',
                zaxis_title='x₃',
                aspectmode='cube',
            ),
            margin=dict(l=0, r=0, t=40, b=0),
        ),
    )
    return fig


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _eigenvector_traces(v, scale):
    v = v / (np.linalg.norm(v) + 1e-15)
    return [
        go.Scatter3d(
            x=[-scale * v[0], scale * v[0]],
            y=[-scale * v[1], scale * v[1]],
            z=[-scale * v[2], scale * v[2]],
            mode='lines',
            line=dict(color='gold', width=5),
            showlegend=False,
        ),
        go.Scatter3d(
            x=[scale * v[0]], y=[scale * v[1]], z=[scale * v[2]],
            mode='markers',
            marker=dict(size=5, color='gold'),
            showlegend=False,
        ),
    ]


def _eigenplane_traces(vector_pair, scale):
    re_v, im_v = vector_pair
    re_v = re_v / (np.linalg.norm(re_v) + 1e-15)
    im_v = im_v / (np.linalg.norm(im_v) + 1e-15)

    u = np.linspace(-scale, scale, 20)
    s, t_grid = np.meshgrid(u, u)
    X = s[:, :, np.newaxis] * re_v + t_grid[:, :, np.newaxis] * im_v

    return [go.Surface(
        x=X[:, :, 0], y=X[:, :, 1], z=X[:, :, 2],
        opacity=0.15,
        colorscale=[[0, 'cyan'], [1, 'cyan']],
        showscale=False,
        showlegend=False,
    )]
