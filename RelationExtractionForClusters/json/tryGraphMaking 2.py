import networkx as nx
import matplotlib.pyplot as plt
import json
from nltk.util import ngrams

def draw_graph(graph, labels=None, graph_layout='spring', node_color='red',
               node_size=600,  node_alpha=0.7,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    G=nx.Graph()

    for edge in graph:
        G.add_edge(edge[0], edge[1])

    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)


    edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                                 label_pos=edge_text_pos)


    plt.show()


dict1={}
templen=0
tempEntity=""
with open('temp.json', 'r') as f:
    dict1=json.loads(f.read())
dict2= dict1['1']
listGraph=[]
listGraphBigram=[]
listEdges=[]
for entries in dict2:
    listGraphBigram.append((entries, len(dict2[entries])))
    if len(dict2[entries])>templen:
            templen=len(dict2[entries])
            tempEntity=entries
    for lists in dict2[entries]:
        
        listGraph.append((entries,lists[1]))
        listEdges.append(lists[0])
print listGraphBigram
print templen
print tempEntity
graph=listGraph
labels=listEdges

draw_graph(graph, labels,'spring','blue')






