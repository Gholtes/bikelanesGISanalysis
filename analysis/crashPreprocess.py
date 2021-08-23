import geopandas

#read in geojson data
incidents = geopandas.read_file("data/Road_Crashes_for_five_Years_-_Victoria.geojson")
print(incidents.columns)
incidents = incidents.loc[incidents["BICYCLIST"] > 0]

incidentFatal = incidents.loc[(incidents["SEVERITY"] =="Fatal accident")]["geometry"]
incidentSerious = incidents.loc[(incidents["SEVERITY"] =="Serious injury accident")]["geometry"]
incidentMinor = incidents.loc[(incidents["SEVERITY"] =="Other injury accident") | (incidents["SEVERITY"] =="Non injury accident")]["geometry"]

incidents.to_file("data/incidents.geojson", driver='GeoJSON')

incidentFatal.to_file("data/incidentFatal.geojson", driver='GeoJSON')

incidentSerious.to_file("data/incidentSerious.geojson", driver='GeoJSON')

incidentMinor.to_file("data/incidentMinor.geojson", driver='GeoJSON')


