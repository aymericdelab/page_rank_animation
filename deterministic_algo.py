#%%
import networkx as nx
import pandas as pd
import random
import pickle
import matplotlib.pyplot as plt
# %%
### create greph:
G = nx.gnm_random_graph(6,12, directed=True)
# %%
## add edges weight
for node, data in G.nodes(data=True):
    data['label'] = str(node)
#%%
for (u,v,w) in G.edges(data=True):
    w['weight'] = round(random.uniform(0,1), 2)
#%%
pos = nx.spring_layout(G)
#%%
node_labels = {node:v['label'] for node,v in G.nodes(data=True)}
edge_labels = {(u,v) : w['weight'] for (u,v,w) in G.edges(data=True)}
plt.figure(figsize=(6,6))
nx.draw(G, pos=pos, labels=node_labels)
nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
plt.axis('off')
plt.show()
#%%
## initialize number of outgoing edges
number_of_outgoing_edges = dict(zip(G.nodes(), [0]*len(G.nodes())))
# calculate number of outgoing edges
for (u,v) in G.edges():
    number_of_outgoing_edges[u]+=1
#%%
children_connections_per_node = dict(zip(G.nodes(), [[] for i in range(len(G.nodes()))]))
for u,v in G.edges():
    children_connections_per_node[u].append(v)
parent_connections_per_node = dict(zip(G.nodes(), [[] for i in range(len(G.nodes()))]))
for u,v in G.edges():
    parent_connections_per_node[v].append(u)
#%%
d = 0.85
max_iter=20
## initialize page_rank score
page_rank_score = {}
for node in G.nodes:
    page_rank_score[node] = 1
## for loop until convergence
N = len(G.nodes())
page_rank_score_history = [page_rank_score.copy()]
for i in range(max_iter):
    for node in G.nodes():
        neighbor_nodes = parent_connections_per_node[node]
        page_rank_sum = sum([(page_rank_score[neighbor_node]/len(neighbor_nodes)) for neighbor_node in neighbor_nodes])
        new_score = (1-d)/N + (d*page_rank_sum)
        page_rank_score[node] = new_score
    page_rank_score_history.append(page_rank_score.copy())
#%%
pickle.dump(page_rank_score_history, open('./output_data/page_rank_score_history.pkl', 'wb'))
#page_rank_score_history

# %%
################# WEIGHTED PAGERANK #################
# %%
d = 0.85
max_iter=200
## initialize page_rank score
page_rank_score = {}
for node in G.nodes:
    page_rank_score[node] = 1
## for loop until convergence
N = len(G.nodes())
page_rank_score_history = [page_rank_score.copy()]
for i in range(max_iter):
    for node in G.nodes():
        neighbor_nodes = parent_connections_per_node[node]
        page_rank_sum=0
        for neighbor_node in neighbor_nodes:
            weight = G.edges()[neighbor_node, node]['weight']
            page_rank_sum += page_rank_score[neighbor_node]*weight
        new_score = (1-d)/N + (d*page_rank_sum)
        page_rank_score[node] = new_score
    page_rank_score_history.append(page_rank_score.copy())
# %%
pickle.dump(page_rank_score_history, open('./output_data/page_rank_weights_score_history.pkl', 'wb'))
# %%
############### WEIGHTED PERSONNALIZED PAGERANK  ###############
personalization_dict = {
    0 : 1,
    1 : 0,
    2 : 0,
    3 : 1,
    4 : 0,
    5 : 0,
}
total_sum = sum(personalization_dict.values())
personalization_probs = {k:(v/total_sum) for k, v in personalization_dict.items()}
#%%
d = 0.85
max_iter=200
## initialize page_rank score
page_rank_score = {}
for node in G.nodes:
    page_rank_score[node] = 1
## for loop until convergence
N = len(G.nodes())
page_rank_score_history = [page_rank_score.copy()]
for i in range(max_iter):
    for node in G.nodes():
        neighbor_nodes = parent_connections_per_node[node]
        page_rank_sum=0
        for neighbor_node in neighbor_nodes:
            weight = G.edges()[neighbor_node, node]['weight']
            page_rank_sum += page_rank_score[neighbor_node]*weight
            prob = personalization_probs[node]
        new_score = (1-d)*prob + (d*page_rank_sum)
        page_rank_score[node] = new_score
    page_rank_score_history.append(page_rank_score.copy())
# %%
pickle.dump(page_rank_score_history, open('./output_data/page_rank_weights_perso_score_history.pkl', 'wb'))
# %%