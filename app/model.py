from bokeh import models

import numpy as np
import requests

from app import config


class Model:
    def __init__(self):
        self.zipcode_to_info = {
            p['navn'] + ', ' + p['nr']: p for p in requests.get(
                'https://api.dataforsyningen.dk/postnumre'
            ).json()
        }
        self._selected_zipcode = None
        self._selected_road = None
        self.addresses = models.ColumnDataSource(data={
            'addresse': [],
            'x': [],
            'y': [],
            'lat': [],
            'lon': [],
        })

    @property
    def selected_zipcode(self):
        return self._selected_zipcode

    @selected_zipcode.setter
    def selected_zipcode(self, value):
        self._selected_zipcode = value
        payload = requests.get(
            'https://api.dataforsyningen.dk/adresser'
            f'?postnr={self.zipcode["nr"]}'
        ).json()
        lat = np.array([p['adgangsadresse']['adgangspunkt']['koordinater'][1] for p in payload])
        lon = np.array([p['adgangsadresse']['adgangspunkt']['koordinater'][0] for p in payload])
        x, y = mercator(lat, lon)
        self.addresses.data = {
            'addresse': [p['adressebetegnelse'] for p in payload],
            'x': x,
            'y': y,
            'lat': lat,
            'lon': lon,
        }

    @property
    def zipcode(self):
        return self.zipcode_to_info[self.selected_zipcode]

    @property
    def zipcode_options(self):
        return sorted(list(self.zipcode_to_info))

    @property
    def llbbox(self):
        if self.selected_zipcode is None:
            return config.DEFAULT_BBOX
        return self.zipcode['bbox']

    @property
    def xybbox(self):
        lon_min, lat_min, lon_max, lat_max  = self.llbbox
        x_min, y_min = mercator(lat_min, lon_min)
        x_max, y_max = mercator(lat_max, lon_max)
        return (x_min, y_min, x_max, y_max)


def mercator(lat, lon):
    r_major = 6378137.000
    x = r_major * np.radians(lon)
    scale = x / lon
    y = (
        180.0 / np.pi * np.log(
            np.tan(
                np.pi / 4.0 + lat * (np.pi / 180.0) / 2.0
            )
        ) * scale
    )
    return (x, y)
