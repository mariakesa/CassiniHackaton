import requests
import geopandas as gpd

class GeoJSONData:
  def __init__(self):
    self.get_data()

  def get_data(self):
    # The URL of the GeoJSON file
    url = 'https://datahub.io/core/geo-countries/r/countries.geojson'
    
    # Fetch the GeoJSON file
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Write the content to a file if you prefer or load it directly
        with open('countries.geojson', 'wb') as f:
            f.write(response.content)
        print("File downloaded successfully")
    else:
        print("Failed to download the file")
  
    self.gdf = gpd.read_file(countries.geojson)

  def filter_by_country(self, country_name):
    morocco_data = self.gdf[self.gdf['ADMIN'] == country_name]
    geometry_data=morocco_data.geometry.__geo_interface__

    geometry_string = json.dumps(geometry_data)
    fields = json.loads(geometry_string)
    return fields

fields=GeoJSONData().filter_by_country("Morocco")
