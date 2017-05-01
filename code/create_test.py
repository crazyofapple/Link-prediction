from graph import Graph
from utils import separate_edge_rate

# read original data as graph
g = Graph("../data/friends.txt")

# load data
g.read()

# separate data as 90% train set and 10% test set
sep = separate_edge_rate(g, 0.1)

# write test set to "test.txt" file
with open("../data/test.txt", "w") as fp:
    for e in sep:
        fp.write("%s\t%s\n" % (e[0], e[1]))

# write train set to "train.txt" file
g.write("../data/train.txt")