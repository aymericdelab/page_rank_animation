#%%
import random 
import networkx as nx
import pandas as pd
import random
import pickle
import matplotlib.pyplot as plt
from PIL import Image
import glob

#%%
# Create the frames
def create_gif(img_path):
    frames = []
    imgs = glob.glob(img_path)
    for i in sorted(imgs):
        new_frame = Image.open(i)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    duration = len(imgs)*200
    frames[0].save('page_rank.gif', format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=600, loop=0)
#%%
def get_colors(G, walker_position):
    color_list = ['r' if node == walker_position else 'b' for node in list(G.nodes())]
    return color_list
#%%
def draw_network(G, pos, scores, color_list, random_walker, step):
    node_labels = {node:v['label'] for node,v in G.nodes(data=True)}
    node_labels = {u: str(u)+' : ' + str(v) for (u,v) in zip(node_labels, scores)}
    edge_labels = {(u,v) : w['weight'] for (u,v,w) in G.edges(data=True)}
    fig = plt.figure(figsize=(6,6))
    chosen_edge = random_walker.chosen_edge
    if chosen_edge is not None:
        edge_weights = [6 if edge==chosen_edge else 2 for edge in G.edges()]
    else:
        edge_weights = len(G.edges())*[2]
    nx.draw(G, pos=pos, labels=node_labels, width=edge_weights)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    nx.draw_networkx_nodes(G, pos=pos, node_color=color_list, node_size=2000)
    damping = random_walker.damping
    text =  'DAMPING!'
    if damping is True:
        plt.text(-1,-0.5, text, font={'family' : 'Comic Sans MS', 'size' : '30'})
    else:
        plt.text(-1,-0.5, len(text)*' ', font={'family' : 'Comic Sans MS', 'size' : '30'})
    plt.text(-1,-0.8, 'Step: {}'.format(str(step)), font={'family' : 'Comic Sans MS', 'size' : '30'})

    plt.axis('off')
    fig.savefig('./images/{}_image.png'.format(step))


#%%
def page_rank(G, max_iter, personalization=None, damping_factor=1, draw=False):
    scores=len(G.nodes())*[0]
    weights={(u,v):w['weight'] for (u,v,w) in G.edges(data=True)}
    random_walker = RandomWalker(G, weights=weights, personalization=personalization, damping_factor=damping_factor)
    random_walker.start()
    for i in range(max_iter):
        if random_walker.position is None:
            random_walker.start()
        else:
            random_walker.next()
        walker_position = random_walker.position
        scores[walker_position]+=1
        if draw is True:
            color_list = get_colors(G, walker_position)
            draw_network(G, pos, scores, color_list, random_walker, step=i)
        else:
            pass
    return scores
#%%
######
class RandomWalker:
    def __init__(self, G, weights=None, personalization=None, damping_factor=1):
        self.G = G
        self.position = None
        self.damping_factor=damping_factor
        self.damping = False
        self.weights = weights
        self.personalization = personalization
        self.chosen_edge=None
    
    def start(self):
        nodes_list = list(self.G.nodes())
        if self.personalization is None:
            start_position = random.choices(nodes_list) 
        else:
            start_position = random.choices(nodes_list, weights=self.personalization) 
        self.position = start_position[0]
    
    def next(self):
        position = self.position
        weights=self.weights
        outgoing_nodes = [v for (u,v) in self.G.edges() if u==position]
        damping_prob = random.uniform(0,1)
        if damping_prob > self.damping_factor:
            self.damping = True
            return self.start()
        elif outgoing_nodes != []:
            if weights is None:
                next_position = random.choices(outgoing_nodes)
            else:
                weight_list=[weights[(self.position, outgoing_node)] for outgoing_node in outgoing_nodes]
                next_position = random.choices(outgoing_nodes, weights=weight_list)
                self.chosen_edge = (position, next_position[0])
            self.damping = False
            self.position = next_position[0]
        else:
            self.damping = False
            return self.start()
#%%
if __name__=='__main__':
    ## create random graph
    G = nx.gnm_random_graph(6,12, directed=True)
    pos = nx.spring_layout(G)

    ## add random weight
    for node, data in G.nodes(data=True):
        data['label'] = str(node)
    for (u,v,w) in G.edges(data=True):
        w['weight'] = round(random.uniform(0,1), 2)

    personalization = [0, 0, 1, 0, 1, 0]
    max_iter=10
    pr_scores = page_rank(G, max_iter, personalization=None, 
        damping_factor=0.85, draw=True)
    ## 
    #create gif
    create_gif("./images/*.png")
