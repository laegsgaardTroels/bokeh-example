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
        spinner_text = """
<!-- https://www.w3schools.com/howto/howto_css_loader.asp -->
<div class="loader">
<style scoped>
.loader {
border: 5px solid #f3f3f3; /* Light grey */
border-top: 5px solid #3498db; /* Blue */
border-radius: 50%;
width: 10px;
height: 10px;
margin-top: 23px;
animation: spin 2s linear infinite;
}

@keyframes spin {
0% { transform: rotate(0deg); }
100% { transform: rotate(360deg); }
}
</style>
</div>"""
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
