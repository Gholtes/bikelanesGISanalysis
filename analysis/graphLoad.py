'''
source: https://networkx.org/documentation/latest/auto_examples/geospatial/plot_lines.html
'''

import geopandas
import matplotlib.pyplot as plt
import momepy
import networkx as nx
from contextily import add_basemap
from libpysal import weights
import random


def navigate(G, u, v):
	shortestPath = nx.algorithms.shortest_paths.generic.shortest_path(G, u, v, weight="mm_len")
	for i, from_node in enumerate(shortestPath[:-2]):
		to_node = shortestPath[i+1]
		G[from_node][to_node]['uses'] += 1


#read in geojson data
bikelanes = geopandas.read_file("data/Principal_Bicycle_Network_cbd.geojson")

#convert to nx
G = momepy.gdf_to_nx(bikelanes, 
	approach="primal", 
	length="mm_len",
	multigraph=False,
	directed=False)

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
for i, u in enumerate(G.nodes):
	for j, v in enumerate(G.nodes):
		if random.random() < 0.005:
			try:
				navigate(G, u, v)
				cnt+=1
				print(cnt)
			except:
				print("Failed to find a path")


#Format vars
maxUses = max([G[u][v]['uses'] for u,v in G.edges])
maxWidth = 3
positions = {n: [n[0], n[1]] for n in list(G.nodes)}
colors = [G[u][v]['color'] for u,v in G.edges]
widths = [((maxWidth * G[u][v]['uses'] )/ maxUses + 1) for u,v in G.edges]

# Plot
f, ax = plt.subplots(1, 2, figsize=(12, 6), sharex=True, sharey=True)
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



# # convert graph back to GeoDataFrames
# W = momepy.nx_to_gdf(G, lines=True)
# print(W)
