import numpy as np
import geopandas as gpd
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
import pandas as pd
from pyproj import CRS
import networkx as nx
from geopandas.tools import sjoin
import sys
import copy
from k_means_constrained import KMeansConstrained



wegenetz_exp = gpd.read_file('glasfiber.shp')
hauspoints = gpd.read_file('houses.shp')



wegenetz_exp.drop(wegenetz_exp.columns.difference(['geometry']), 1, inplace=True)

wegenetz_exp['dis'] = 0

wegenetz_dis = wegenetz_exp.dissolve(by='dis', aggfunc='sum')
wegenetz_exp = wegenetz_dis.explode()
wegenetz_exp = wegenetz_exp.reset_index()


wegenetz_exp['laenge'] = wegenetz_exp['geometry'].length.round(2)
wegenetz_exp['order'] = wegenetz_exp.index

hauspoints.drop(hauspoints.columns.difference(['geometry']), 1, inplace=True)
haus_original = copy.deepcopy(hauspoints)
hauspoints['original'] = hauspoints.index



bg = nx.Graph()
bg.graph['crs'] = wegenetz_exp.crs
fields = list(wegenetz_exp.columns)

for index, row in wegenetz_exp.iterrows():
   first = row.geometry.coords[0]
   last = row.geometry.coords[-1]

   data = [row[f] for f in fields]
   attributes = dict(zip(fields, data))
   bg.add_edge(first, last, **attributes)

first = list(bg.edges(data=True))

big_G = nx.Graph()
for data in first:
   big_G.add_edge(data[0],data[1], order = data[2]['order'] , weight=data[2]['laenge'])

if nx.is_connected(big_G) == False:
   sys.exit('The wegenetz doesnt have the enough quality to build the Tiefbau. Please modify the settings of wegenetz cleaning')
     

node_xy, node_data = zip(*big_G.nodes(data=True))
point = gpd.GeoDataFrame(list(node_data), geometry=[Point(i, j) for i, j in node_xy])
point.crs = CRS.from_epsg(25832).to_wkt()

mapping = dict(zip(big_G, range(0, len(big_G))))
big_G = nx.relabel_nodes(big_G, mapping)

edge_labels_exp = nx.get_edge_attributes(big_G, 'order')

#####---------------------------------------------------------------------------

join = sjoin(hauspoints, point, how='left') 

second = MultiPoint(point.geometry)
for i in range(len(hauspoints)):
    if pd.isna(join.loc[i,'index_right'])==True:
        first = hauspoints.loc[i,'geometry']
        nearest_geoms = nearest_points(first, second)
        hauspoints.loc[i,'geometry'] = nearest_geoms[1]
        #print (i)

join = sjoin(hauspoints, point,how='left') 
hauspoints['network_id'] = join['index_right']
#-----------------------------------------------------------------------------


          
nodes_unique = pd.Series(hauspoints['network_id'])
nodes_unique.index = nodes_unique.values

white = hauspoints['network_id'].to_list()

bignes = len(hauspoints)

am = pd.DataFrame(np.zeros(shape=(bignes,bignes)), columns=nodes_unique, index=nodes_unique)
for i in nodes_unique:
    short = nx.single_source_dijkstra_path_length(big_G, i, cutoff=4000, weight='weight')
    am[i] = [short[p] if p in short else 0 for p in nodes_unique]

db = KMeansConstrained(n_clusters = 4,size_max=20,random_state=0)
hauspoints.insert(2, 'cc_cluster', list(db.fit_predict(am)))




hauspoints.to_file('output.shp')

#######---------------------------------------------------------------------------------------------------
