# Copyright 2015 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""

======
Map
======

.. currentmodule:: bqplot.map

.. autosummary::
   :toctree: generate/

   Map
"""

from IPython.utils.traitlets import Unicode, List, Dict, Float, Bool, Instance
from IPython.html.widgets import DOMWidget, CallbackDispatcher

from .scales import ColorScale
from .axes import Axis


class Map(DOMWidget):

    """Class to generate a waffle wrapped map of the list of data provided.

    Map Drawing Attributes
    ------------------
    map_width: int
        minimum width of the entire map
    map_height: int
        minimum height of the entire map
    map_margin: dict
        margin for the market map plot area with respect to the entire display
        area
    preserve_aspect: bool
        boolean to control if the aspect ratio should be preserved or not
        during a resize
    cols: int
        Suggestion for no of columns in the map.If not specified, value is
        inferred from the no of rows and no of cells
    rows: int
        No of rows in the map.If not specified, value is inferred from the no
        of cells and no of columns.
        If both rows and columns are not specified, then a square is
        constructed basing on the no of cells.
        The above two attributes are suggestions which are respected unless
        they are not feasible. One required condition is that, the number of
        columns is odd when row_groups is greater than 1.
    row_groups: int
        No of groups the rows should be divided into. This can be used to draw
        more square cells for each of the groups

    Display Attributes
    ------------------
    colors: list of colors
        colors for each of the groups which are cycled over to cover all the
        groups
    stroke: color
        Stroke of each of the cells of the market map
    group_stroke: color
        Stroke of the border for the group of cells corresponding to a group
    selected_stroke: color
        stroke for the selected cells
    hovered_stroke: color
        stroke for the cell being hovered on

    Other Attributes
    ----------------
    enable_select: bool
        boolean to control the ability to select the cells of the map by
        clicking
    enable_hover: bool
        boolean to control if the map should be aware of which cell is being
        hovered on. If it is set to False, tooltip will not be displayed
    """
    fig_margin = Dict(dict(top=0, bottom=20, left=50, right=50), sync=True)   # Margin with respect to the parent. Width, height etc are determined by this
    min_width = Float(800, sync=True)
    min_height = Float(600, sync=True)
    enable_hover = Bool(True, sync=True)
    hover_fill = Unicode("Orange", sync=True, allow_none=True)
    hover_stroke = Unicode("", sync=True, allow_none=True)
    hover_stroke_width = Float(5.0, sync=True)
    stroke_color = Unicode("White", sync=True)
    color = Unicode("DodgerBlue", sync=True)
    color_data = Dict(sync=True)
    color_scale = Instance(ColorScale, sync=True)
    _view_name = Unicode("Map", sync=True)
    enable_select = Bool(True, sync=True)
    selected = List([], sync=True)
    selected_fill = Unicode("Red", sync=True, allow_none=True)
    selected_stroke = Unicode("", sync=True, allow_none=True)
    selected_stroke_width = Float(5.0, sync=True)
    axis = Instance(Axis, sync=True)
    tooltip_color = Unicode("White", sync=True)
    display_tooltip = Bool(True, sync=True)
    text_data = Dict(sync=True)
    text_color = Unicode("Black", sync=True)
    text_format = Unicode(".2f", sync=True)

    def __init__(self, **kwargs):
        """Constructor for WorldMapWidget"""
        super(Map, self).__init__(**kwargs)
        self._ctrl_click_handlers = CallbackDispatcher()
        self._hover_handlers = CallbackDispatcher()
        self.on_msg(self._handle_button_msg)

    def on_ctrl_click(self, callback, remove=False):
        self._ctrl_click_handlers.register_callback(callback, remove=remove)

    def on_hover(self, callback, remove=False):
        self._hover_handlers.register_callback(callback, remove=remove)

    def _handle_button_msg(self, _, content):
        if content.get('event', '') == 'click':
            self._ctrl_click_handlers(self, content)
        if content.get('event', '') == 'hover':
            self._hover_handlers(self, content)
