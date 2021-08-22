import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import momepy
import networkx as nx
from contextily import add_basemap
from libpysal import weights
import random

pointsperSA2 = 10
pointsPerflow = 3

print("Loading data...")
#Load SA info
SA4 = ['Melbourne - Inner', 'Melbourne - Inner East',
 'Melbourne - Inner South', 'Melbourne - North East',
 'Melbourne - North West', 'Melbourne - Outer East'
 'Melbourne - South East', 'Melbourne - West']

# SA4 = ['Melbourne - Inner', 'Melbourne - Inner East',
#  'Melbourne - Inner South']

sa = pd.read_csv("data/SA2_2011_AUST.csv")
sa = sa[sa["SA4_NAME_2011"].isin(SA4)]
SA2 = list(sa["SA2_NAME_2011"].unique())

#Load SA shapes
sa2 = geopandas.read_file("data/1270055001_sa2_2016_aust_shape")
sa2 = sa2[["SA2_NAME16", 'geometry']]
sa2 = sa2[sa2["SA2_NAME16"].isin(SA2)]

print(sa2.total_bounds)

#Load commute flows
flows = pd.read_csv("data/commuteflowAll.csv")
#fill in missing placenames
flows = flows.ffill(axis = 0)
flows = flows[flows["SA2_UR"].isin(SA2)]
flows = flows[flows["SA2_POW"].isin(SA2)]

#Load bikelanes
bikelanes = geopandas.read_file("data/Principal_Bicycle_Network_(PBN).geojson")
print("Data loaded")
#Spacial join on SA2
print("Data processing...")
bikelanes = geopandas.sjoin(bikelanes, sa2, how="inner", op='intersects')

G = momepy.gdf_to_nx(bikelanes, 
	approach="primal", 
	length="mm_len",
	multigraph=False,
	directed=False)

print("Data ready to use")

print("Selecting points by SA2")
#Select start points per suburb
SA2_valid_locations = {}
for u, v in G.edges:
	status = G[u][v]['status']
	SA2_edge = G[u][v]['SA2_NAME16']
	if status == "Existing":
		if SA2_edge in SA2_valid_locations:
			if len(SA2_valid_locations[SA2_edge]) < pointsperSA2 and random.random() < 0.25: #dont add them all!
				SA2_valid_locations[SA2_edge].append(u)
		else:
			SA2_valid_locations[SA2_edge] = [u]


print("Allocating routes to flows")
routes = []
for UR in SA2_valid_locations.keys():
	for POW in SA2_valid_locations.keys():
		#get flows by bike between the SA2s
		bikeflow = int(flows[(flows["SA2_UR"] == UR) & (flows["SA2_POW"] == POW)]["Bicycle"])
		allflow = int(flows[(flows["SA2_UR"] == UR) & (flows["SA2_POW"] == POW)]["Total"])
		if bikeflow == 0: #skip zero flow cases (unridable)
			continue
		bike_count_route = bikeflow / pointsPerflow
		all_count_route = allflow / pointsPerflow
		for i in range(pointsPerflow):
			UR_coordinates = random.choice(SA2_valid_locations[UR])
			POW_coordinates = random.choice(SA2_valid_locations[POW])
			routes.append([UR_coordinates, POW_coordinates, UR, POW, bike_count_route, all_count_route])

routes = pd.DataFrame.from_records(routes)
routes.columns = ["UR", "POW", "UR_SA2", "POW_SA2", "Bikes", "Total"]
routes.to_csv("data/routes.csv", index=False)
