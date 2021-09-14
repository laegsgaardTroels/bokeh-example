from bokeh import events
from bokeh import layouts
from bokeh import models as bm

import math
import requests

from app import model
from app import views


class Main:
    def __init__(self):
        self.model = model.Model()
        self.map = views.WorldMap(self.model)
        self.setup_controls()
        self.layout = layouts.row(children=[])

    def refresh(self):
        self.map.refresh()
        self.layout.children = [
            self.controls,
            self.map.layout,
        ]
        self.div_spinner.text = ""

    def setup_controls(self):
        zipcode = bm.Select(
            title="POSTNR",
            value=self.model.selected_zipcode,
            options=self.model.zipcode_options,
        )
        zipcode.on_change(
            'value',
            self.zipcode_handler,
        )
        self.div_spinner = bm.widgets.Div(text="", width=10, height=10)
        self.controls = layouts.row(
            children=[
                zipcode,
                self.div_spinner
            ],
            width=400
        )

    def zipcode_handler(self, attr, old, new):
        spinner_text = '<div class="loader"></div>'
        self.div_spinner.text = spinner_text
        def update():
            self.model.selected_zipcode = new
            x_min, y_min, x_max, y_max = self.model.xybbox
            self.map.plot.x_range.update(start=x_min, end=x_max)
            self.map.plot.y_range.update(start=y_min, end=y_max)
            self.div_spinner.text = ""
        curdoc().add_next_tick_callback(update)


from bokeh.io import curdoc
main = Main()
main.refresh()
curdoc().add_root(main.layout)
