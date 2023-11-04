import json
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal
import numpy as np

import openeo

class CalculateTimeseriesP6ltsamaa:
    def __init__(self):
        self.make_connection()

    def make_connection(self):
        self.connection = openeo.connect(url="openeo.dataspace.copernicus.eu")
        self.connection.authenticate_oidc()

    def make_cube(self):
        self.s2cube = self.connection.load_collection(
            "SENTINEL2_L2A",
            temporal_extent==["2019-01-01", "2023-11-04"],
            bands=["B03","B04", "B08"],
        )

    def calculate_ndvi(self):
        red = self.s2cube.band("B04")
        nir = self.s2cube.band("B08")
        self.ndvi = (nir - red) / (nir + red)

    def calculate_ndwi(self):
        red = self.s2cube.band("B03")
        nir = self.s2cube.band("B08")
        self.ndwi = (nir - red) / (nir + red)

    def run_pipeline(self, fields):
        self.make_cube()
        self.calculate_ndvi()
        self.calculate_ndwi()
        #Calculate ndvi and save
        timeseries_ndvi = self.ndvi.aggregate_spatial(geometries=fields, reducer="mean")
        job = timeseries_ndvi.execute_batch(out_format="CSV", title="NDVI timeseries")
        job.get_results().download_file("ndvi-results/ndvi-p6ltsamaa.csv")
        #Calculate ndwi and save
        timeseries_ndwi = self.ndwi.aggregate_spatial(geometries=fields, reducer="mean")
        job = timeseries_ndwi.execute_batch(out_format="CSV", title="NDWI timeseries")
        job.get_results().download_file("ndvi-results/ndwi-p6ltsamaa.csv")
      
#Drought data from Jamame (Jamaame) region of Kenya.
fields=json.loads("""
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            [
              25.96574190256925,
              58.672515617740316
            ],
            [
              25.96574190256925,
              58.66050153787188
            ],
            [
              25.99985205482895,
              58.66050153787188
            ],
            [
              25.99985205482895,
              58.672515617740316
            ],
            [
              25.96574190256925,
              58.672515617740316
            ]
          ]
        ],
        "type": "Polygon"
      }
    }
  ]
}
""")
      
CalculateTimeseriesP6ltsamaa().run_pipeline(fields)
