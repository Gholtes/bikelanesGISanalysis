'''
source: https://networkx.org/documentation/latest/auto_examples/geospatial/plot_lines.html
'''

import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import momepy
import networkx as nx
from contextily import add_basemap
from libpysal import weights
import random
import time


def navigate(G, u, v, weight):
	'''Find the shortest path between nodes, and update path usage
	Performance tests: 
		.generic.shortest_path: 16ms per path
		.astar.astar_path: 21ms per path'''
	shortestPath = nx.algorithms.shortest_paths.generic.shortest_path(G, u, v, weight="mm_len")
	# shortestPath = nx.algorithms.shortest_paths.astar.astar_path(G, u, v, weight="mm_len")
	for i, from_node in enumerate(shortestPath[:-2]):
		to_node = shortestPath[i+1]
		G[from_node][to_node]['uses'] += weight


def removeRedundantNodes(G):
	pass
	# for node in G.nodes:
	# 	if G.degree(node) == 2:

# melbourneBounds = [144.33363405, -38.08499998, 145.58004258, -37.17509899]
melbourneBounds = [144.70645662, -38.1092582,  145.36253358, -37.45318124]
melbourneBounds = [144.80645662, -38.0092582,  145.26253358, -37.55318124]


#read in geojson data
bikelanes = geopandas.read_file("data/Principal_Bicycle_Network_(PBN).geojson")
# bikelanes = geopandas.read_file("Principal_Bicycle_Network_cbd.geojson")

left, bottom, right, top = melbourneBounds
bikelanes = bikelanes.cx[left:right, bottom:top] #restrict area of interest
bikelanes = bikelanes.explode() #split the few multipart geometries that exist

routes = pd.read_csv("data/routes.csv")
print(bikelanes.total_bounds)

#convert to nx
G = momepy.gdf_to_nx(bikelanes, 
	approach="primal", 
	length="mm_len",
	multigraph=False,
	directed=False)

#clean graph
G.remove_edges_from(nx.selfloop_edges(G))

print("Graph loaded")

#access and process edge attributes
for u, v in G.edges:
	status = G[u][v]['status']
	if status == "Proposed" or status == "Intended":
		G[u][v]['color'] = 'r'
	else:
		G[u][v]['color'] = 'g'
	G[u][v]['uses'] = 0

cnt = 0
st = time.time()
for row in routes.iterrows():
	start = tuple([float(x.strip("()")) for x in row[1]["UR"].split(",")])
	end = tuple([float(x.strip("()")) for x in row[1]["POW"].split(",")])
	uses = float(row[1]["Bikes"])
	# if cnt > 100:
	# 	break
	try:
		navigate(G, start, end, uses)
		cnt+=1
		if cnt % 50 == 0:
			print(cnt)
	except:
		pass
		# print("Failed to find a path")

print("time taken to simulate: ",time.time()-st)

#Format vars
maxUses = max([G[u][v]['uses'] for u,v in G.edges])
maxWidth = 5
positions = {n: [n[0], n[1]] for n in list(G.nodes)}
colors = [G[u][v]['color'] for u,v in G.edges]
widths = [((maxWidth * G[u][v]['uses'] )/ maxUses + 0.3) for u,v in G.edges]

# Plot graphs
f, ax = plt.subplots(1, 2, figsize=(60, 30), sharex=True, sharey=True)
bikelanes.plot(color="k", ax=ax[0])
for i, facet in enumerate(ax):
    facet.set_title(("Map", "Graph")[i])
    facet.axis("off")
nx.draw(G, 
		positions, 
		ax=ax[1], 
		node_size=0, 
		edge_color=colors, 
		width=widths)
f.savefig("graph.png")


# convert graph back to GeoDataFrames
points, lines = momepy.nx_to_gdf(G, lines=True, spatial_weights=False)
lines.to_file("data/bikelanes.geojson", driver='GeoJSON')


