"""
controls.py — Module 4: ipywidgets UI for live interactive phase portraits.

Wires matrix entry sliders, initial condition controls, and display toggles
to the solver + renderer pipeline. The Plotly figure updates in-place on any
widget change.
"""

import numpy as np
import ipywidgets as widgets
from IPython.display import display
import plotly.graph_objects as go

from solver import analyze, integrate_many
from colormap_utils import compute_color_values_many


# ---------------------------------------------------------------------------
# Default initial conditions
# ---------------------------------------------------------------------------

_DEFAULT_X0 = [
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
]


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def make_controls(
    A_init=None,
    x0_list=None,
    t_max_init=10.0,
    quantity='speed',
    colormap='plasma',
    n_points=500,
):
    """
    Build and display the full interactive widget panel.

    Parameters
    ----------
    A_init     : array-like (3, 3) or None  — initial matrix (default: identity)
    x0_list    : list of length-3 lists or None — initial conditions
    t_max_init : float — initial integration end time
    quantity   : 'speed' | 'time' | 'distance' — 4D color encoding
    colormap   : str — Plotly colorscale name
    n_points   : int — trajectory resolution
    """
    if A_init is None:
        A_init = np.eye(3)
    A_init = np.asarray(A_init, dtype=float)

    if x0_list is None:
        x0_list = [list(x) for x in _DEFAULT_X0]

    # -----------------------------------------------------------------------
    # Matrix entry sliders (3×3 grid)
    # -----------------------------------------------------------------------
    entry_sliders = {}
    for i in range(3):
        for j in range(3):
            key = (i, j)
            entry_sliders[key] = widgets.FloatSlider(
                value=float(A_init[i, j]),
                min=-5.0, max=5.0, step=0.1,
                description=f'a{i+1}{j+1}',
                continuous_update=False,
                style={'description_width': '30px'},
                layout=widgets.Layout(width='200px'),
            )

    matrix_grid = widgets.GridBox(
        [entry_sliders[(i, j)] for i in range(3) for j in range(3)],
        layout=widgets.Layout(
            grid_template_columns='repeat(3, 210px)',
            grid_gap='4px 4px',
        ),
    )
    matrix_label = widgets.HTML('<b>Matrix A</b>')

    # -----------------------------------------------------------------------
    # Time range slider
    # -----------------------------------------------------------------------
    t_max_slider = widgets.FloatSlider(
        value=t_max_init, min=1.0, max=50.0, step=0.5,
        description='t max',
        continuous_update=False,
        style={'description_width': '50px'},
        layout=widgets.Layout(width='350px'),
    )

    # -----------------------------------------------------------------------
    # Initial conditions — editable text boxes
    # -----------------------------------------------------------------------
    ic_inputs = []   # list of 3-tuples of BoundedFloatText
    ic_rows = []     # list of HBox widgets (one per IC)

    def _make_ic_row(x0):
        boxes = tuple(
            widgets.BoundedFloatText(
                value=float(v), min=-20.0, max=20.0, step=0.1,
                layout=widgets.Layout(width='80px'),
            )
            for v in x0
        )
        for box in boxes:
            box.observe(_on_change, names='value')
        row = widgets.HBox(list(boxes))
        ic_inputs.append(boxes)
        ic_rows.append(row)
        return row

    add_ic_btn = widgets.Button(description='+ Add IC', button_style='info',
                                layout=widgets.Layout(width='100px'))
    remove_ic_btn = widgets.Button(description='- Remove IC', button_style='warning',
                                   layout=widgets.Layout(width='110px'))
    ic_container = widgets.VBox([])
    ic_label = widgets.HTML('<b>Initial conditions  (x₁, x₂, x₃)</b>')

    for x0 in x0_list:
        ic_container.children = (*ic_container.children, _make_ic_row(x0))

    # -----------------------------------------------------------------------
    # Toggle checkboxes
    # -----------------------------------------------------------------------
    chk_eigvec = widgets.Checkbox(value=True, description='Show eigenvectors',
                                  indent=False, layout=widgets.Layout(width='175px'))
    chk_eigplane = widgets.Checkbox(value=True, description='Show eigenplanes',
                                    indent=False, layout=widgets.Layout(width='175px'))
    chk_colorbar = widgets.Checkbox(value=True, description='Show colorbar',
                                    indent=False, layout=widgets.Layout(width='175px'))
    toggles = widgets.HBox([chk_eigvec, chk_eigplane, chk_colorbar])

    # -----------------------------------------------------------------------
    # Plotly FigureWidget (updates in-place without re-rendering the cell)
    # -----------------------------------------------------------------------
    fw = go.FigureWidget()
    _build_figure(fw, entry_sliders, ic_inputs, t_max_slider,
                  chk_eigvec, chk_eigplane, chk_colorbar,
                  quantity, colormap, n_points)

    # -----------------------------------------------------------------------
    # Callbacks
    # -----------------------------------------------------------------------
    def _on_change(change=None):
        _build_figure(fw, entry_sliders, ic_inputs, t_max_slider,
                      chk_eigvec, chk_eigplane, chk_colorbar,
                      quantity, colormap, n_points)

    def _on_add_ic(_):
        ic_container.children = (*ic_container.children,
                                  _make_ic_row([1.0, 0.0, 0.0]))
        _on_change()

    def _on_remove_ic(_):
        if len(ic_inputs) > 1:
            ic_inputs.pop()
            ic_rows.pop()
            ic_container.children = ic_container.children[:-1]
            _on_change()

    for slider in entry_sliders.values():
        slider.observe(_on_change, names='value')
    t_max_slider.observe(_on_change, names='value')
    chk_eigvec.observe(_on_change, names='value')
    chk_eigplane.observe(_on_change, names='value')
    chk_colorbar.observe(_on_change, names='value')
    add_ic_btn.on_click(_on_add_ic)
    remove_ic_btn.on_click(_on_remove_ic)

    # -----------------------------------------------------------------------
    # Layout
    # -----------------------------------------------------------------------
    ic_buttons = widgets.HBox([add_ic_btn, remove_ic_btn])
    panel = widgets.VBox([
        matrix_label,
        matrix_grid,
        widgets.HTML('<hr style="margin:6px 0">'),
        ic_label,
        ic_container,
        ic_buttons,
        widgets.HTML('<hr style="margin:6px 0">'),
        t_max_slider,
        toggles,
    ])

    display(widgets.HBox([panel, fw]))


# ---------------------------------------------------------------------------
# Internal: rebuild the FigureWidget in-place
# ---------------------------------------------------------------------------

def _build_figure(fw, entry_sliders, ic_inputs, t_max_slider,
                  chk_eigvec, chk_eigplane, chk_colorbar,
                  quantity, colormap, n_points):
    # Read current matrix
    A = np.array([[entry_sliders[(i, j)].value for j in range(3)]
                  for i in range(3)], dtype=float)

    # Read current initial conditions
    x0_list = [[box.value for box in row] for row in ic_inputs]

    t_span = (0.0, t_max_slider.value)

    try:
        _, eigen_info = analyze(A)
        trajectories = integrate_many(A, x0_list, t_span=t_span, n_points=n_points)
        color_values = compute_color_values_many(A, trajectories, quantity=quantity)
    except Exception as e:
        # On singular or badly conditioned matrices just clear the plot
        with fw.batch_update():
            fw.data = []
            fw.layout.title = f'Error: {e}'
        return

    # Import renderer here to avoid circular imports at module level
    from renderer import plot_phase_portrait
    new_fig = plot_phase_portrait(
        trajectories=trajectories,
        eigen_info=eigen_info,
        color_values=color_values,
        colormap=colormap,
        show_eigenvectors=chk_eigvec.value,
        show_eigenplanes=chk_eigplane.value,
        show_colorbar=chk_colorbar.value,
    )

    with fw.batch_update():
        fw.data = new_fig.data
        fw.layout = new_fig.layout
