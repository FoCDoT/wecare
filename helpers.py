import networkx as nx
import pickle
import plotly.plotly as py
import plotly
import random
from plotly.graph_objs import *
from plotly.offline import init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)


map_10_dict = {
	0:{'pos':(76,390), 'connections': []},
    1:{'pos':(96,272), 'connections': []},
    2:{'pos':(185,285), 'connections': []},
    3:{'pos':(87,226), 'connections': []},
    4:{'pos':(199,251), 'connections': []},
    5:{'pos':(99,142), 'connections': []},
    6:{'pos':(207,159), 'connections': []},
    7:{'pos':(108,65), 'connections': []},
    8:{'pos':(244,77), 'connections': []},
    9:{'pos':(310,55), 'connections': []},
    10:{'pos':(330,162), 'connections': []},
    11:{'pos':(308,161), 'connections': []},
    12:{'pos':(408,42), 'connections': []},
    13:{'pos':(447,96), 'connections': []},
    14:{'pos':(484,124), 'connections': []},
    15:{'pos':(547,140), 'connections': []},
    16:{'pos':(632,161), 'connections': []},
    17:{'pos':(698,184), 'connections': []},
    18:{'pos':(723,124), 'connections': []},
    19:{'pos':(790,86), 'connections': []},
    20:{'pos':(828,64), 'connections': []},
    21:{'pos':(827,62), 'connections': []},
    22:{'pos':(743,23), 'connections': []},
    23:{'pos':(685,58), 'connections': []},
    24:{'pos':(579,42), 'connections': []},
    25:{'pos':(565,80), 'connections': []},
    26:{'pos':(648,95), 'connections': []},
    27:{'pos':(588,273), 'connections': []},
    28:{'pos':(518,259), 'connections': []},
    29:{'pos':(541,510), 'connections': []},
    30:{'pos':(589,409), 'connections': []},
    31:{'pos':(446,235), 'connections': []},
    32:{'pos':(361,254), 'connections': []},
    33:{'pos':(493,373), 'connections': []},
    34:{'pos':(445,439), 'connections': []},
    35:{'pos':(510,522), 'connections': []},
    36:{'pos':(57,61), 'connections': []},
    37:{'pos':(64,40), 'connections': []},
    38:{'pos':(219,420), 'connections': []},
    39:{'pos':(503,317), 'connections': []},
    40:{'pos':(349,389), 'connections': []},
    41:{'pos':(225,348), 'connections': []}
}


""""""
map_40_dict = {
	0: {'pos': (76, 390), 'connections': []}, 
}


class Map:
	def __init__(self, G):
		self._graph = G
		self.intersections = nx.get_node_attributes(G, "pos")
		self.roads = [list(G[node]) for node in G.nodes()]

	def save(self, filename):
		with open(filename, 'wb') as f:
			pickle.dump(self._graph, f)

def load_map_graph(map_dict):
	G = nx.Graph()
	for node in map_dict.keys():
		G.add_node(node, pos=map_dict[node]['pos'])
	for node in map_dict.keys():
		for con_node in map_dict[node]['connections']:
			G.add_edge(node, con_node)
	return G

def load_map_10():
	G = load_map_graph(map_10_dict)
	return Map(G)

def load_map_40():
	G = load_map_graph(map_40_dict)
	return Map(G)

def show_map(M, start=None, goal=None, path=None):
    G = M._graph
    pos = nx.get_node_attributes(G, 'pos')
    abx = []
    aby = []

    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        abx += [x0, x1, None]
        aby += [y0, y1, None]
    

    edge_trace = Scatter(
    x=abx,
    y=aby,
    line=Line(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

    aax = []
    aay = []

    
    for node in G.nodes():
        x, y = G.node[node]['pos']
        aax.append(x)
        aay.append(y)


    ab1 = []
    ab2 = []


    for node, adjacencies in enumerate(G.adjacency_list()):
        color = 0
        if path and node in path:
            color = 2
        if node == start:
            color = 3
        elif node == goal:
            color = 1
        #node_trace['marker']['color'].append(len(adjacencies))
        #ab1.append(len(adjacencies))
        #node_trace['marker']['color'].append(color)
        ab1.append(color)
        node_info = "Intersection " + str(node)
        #node_trace['text'].append(node_info)
        ab2.append(node_info)

    
    node_trace = Scatter(
        x=aax,
        y=aay,
        text=ab2,
        mode='markers',
        hoverinfo='text',
        marker=Marker(
            showscale=False,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='Hot',
            reversescale=True,
            color=ab1,
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    


    fig = Figure(data=Data([edge_trace,node_trace]),
                 layout=Layout(
                    title='<br>Ambulance path',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                   
                    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))
    #print(plotly.offline.plot(fig,output_type = "div", include_plotlyjs=False))
    iplot(fig)