import geopandas

#read in geojson data
map = geopandas.read_file("data/bikelanes.geojson")
print(map.columns)

map = map[["status", "uses", "geometry"]]
print(map.columns)

map.to_file("data/bikelanesWeb.geojson", driver='GeoJSON')