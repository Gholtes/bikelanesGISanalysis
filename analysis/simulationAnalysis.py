import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import momepy
import networkx as nx
from contextily import add_basemap
from libpysal import weights
import random
import time

#load post-simulation routes
bikelanes = geopandas.read_file("data/bikelanes.geojson")
