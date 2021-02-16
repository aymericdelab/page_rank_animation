## PAGE RANK 

Two things are random in the pagerank algorithm:
- the random walk process of a surfer going from node to node through their edges.
- the value of each node (or their rank)

The random walk process becomes deterministic after an infinite number of iterations. That is why we can calculate the algorithm with a deterministic result. (you can compare that to throwing a coin an infinite number of times. The probability is 50%)

Going through the edges of the graph is like throwing a coin.


### Personalization Vector
The personnalization vector indicates which nodes will be used as outedges by the dangling nodes.
The outedges to be assigned to any “dangling” nodes, i.e., nodes without any outedges. The dict key is the node the outedge points to and the dict value is the weight of that outedge. By default, dangling nodes are given outedges according to the personalization vector (uniform if not specified). This must be selected to result in an irreducible transition matrix (see notes under google_matrix). It may be common to have the dangling dict to be the same as the personalization dict.