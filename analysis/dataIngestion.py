'''
source: https://networkx.org/documentation/latest/auto_examples/geospatial/plot_lines.html
'''

import geopandas
import matplotlib.pyplot as plt
import momepy
import networkx as nx
from contextily import add_basemap
from libpysal import weights

#read in geojson data
bikelanes = geopandas.read_file("data/Principal_Bicycle_Network_(PBN).geojson")

# bikelanes = bikelanes.to_crs()
print("Data loaded")

#subset data:
print("Original bounds: ", bikelanes.total_bounds)
# bikelanes = bikelanes.cx[144.72064551:145.34251942, -38.26697046:-37.61920932]
top, left, bottom, right = -37.78903, 144.942327, -37.821358, 144.974655
bikelanes = bikelanes.cx[left:right, bottom:top]
print("Subset bounds: ", bikelanes.total_bounds)

bikelanes.to_file("data/Principal_Bicycle_Network_cbd.geojson", driver='GeoJSON')


