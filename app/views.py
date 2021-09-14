from bokeh import plotting
from bokeh import tile_providers
from bokeh import layouts
from bokeh import models as bm

from app import config


class View:
    def __init__(self, model):
        self.model = model
        self.layout = layouts.row(children=[], width=config.WIDTH)

    def refresh(self):
        raise NotImplementedError("Implement this in subclass...")


class WorldMap(View):
    """A map used to display the location of object on a world map."""

    def refresh(self):
        x_min, y_min, x_max, y_max = self.model.xybbox
        pan_tool = bm.PanTool()
        wheel_zoom_tool = bm.WheelZoomTool(
            zoom_on_axis=False
        )
        self.plot = plotting.figure(
            title='Real Estate Valuation',
            x_range=(x_min, x_max),
            y_range=(y_min, y_max),
            x_axis_type="mercator",
            y_axis_type="mercator",
            x_axis_label='Longitude [deg]',
            y_axis_label='Latitude [deg]',
            output_backend="webgl",
            tools=[
                pan_tool,
                bm.BoxSelectTool(),
                wheel_zoom_tool,
                bm.ResetTool(),
                bm.HoverTool(
                    tooltips = [
                        ("Address", "@addresse"),
                        ("Latitude", "@lat"),
                        ("Longitude", "@lon"),
                    ]
                ),
            ],
            active_drag=pan_tool,
            active_scroll=wheel_zoom_tool,
            active_inspect=[],
        )
        self.plot.add_tile(
            tile_providers.get_provider(
                tile_providers.CARTODBPOSITRON_RETINA
            )
        )
        self.plot.circle(
            x='x',
            y='y',
            size=5,
            fill_color="blue",
            fill_alpha=0.6,
            source=self.model.addresses,
        )
        self.plot.toolbar.logo = None
        self.layout.children = [self.plot]
