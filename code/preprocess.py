#encoding:utf-8

from __future__ import division
from graph import Graph

class Model:
    def __init__(self, graph):
        self.__graph = graph
        self.__conns = {}

    def find_latent_friends(self):
        for ni in self.__graph.all_nodes():
            if ni % 100 == 0: print ni
            if not self.__conns.has_key(ni):
                self.__conns[ni] = {}
            fringe_nodes = set(self.__graph.node(ni).keys())
            for k in range(2,4):
                fringe_nodes = self.find_kdegree_friends(ni, fringe_nodes, k)
                for nj in fringe_nodes:
                    if self.__graph.edge(ni, nj) is None and not self.__conns[ni].has_key(nj):
                        self.__conns[ni][nj] = k
        filename = '../data/friends_latent.txt'
        with open(filename, 'w') as fp:
            for nodei, items in self.__conns.iteritems():
                for nodej, dist in items.iteritems():
                    fp.write('%d\t%d\t%d\n'%(nodei, nodej, dist))
            fp.close()

    # 查找k度人脉
    def find_kdegree_friends(self, me, nodes, k):
        kfriends = {}
        if k > 1:
            for node in nodes:
                fringe_nodes = set(self.__graph.node(node).keys())
                for nj in fringe_nodes:
                    if me == nj: continue
                    else:
                        #cmn_friends = self.find_common_friends(fringe_nodes, set(self.__graph.node(nj).keys()))
                        kfriends[nj] = 1
        #kfriends = sorted(kfriends.iteritems(), key=lambda x:x[1], reverse=True)
        return set(kfriends.keys())

    def find_common_friends(self, nodes_a, nodes_b):
        return len(nodes_a & nodes_b)
#返回边集
def load_data_list(filename):
    dataset = []
    with open(filename, "r") as fp:
        data = fp.read()
        if "\r\n" in data:
            data_list = data.split("\r\n")
        else:
            data_list = data.split("\n")
        for s in data_list:
            comment_index = s.find("#")
            if comment_index != -1:
                s = s[: comment_index]
            if len(s) == 0: continue
            s = s.replace(" ", "\t")
            tup = tuple(s.split("\t"))
            temp_tup = []
            for t in tup:
                if t.find('.') != -1: temp_tup.append(float(t))
                else: temp_tup.append(int(t))
            dataset.append(tuple(temp_tup))
    return dataset
#返回去重后边集
def load_data_set(filename):
    return set(load_data_list(filename))

#返回与node相连节点的链表
def load_data_dict(filename):
    dataset = {}
    with open(filename, "r") as fp:
        data = fp.read()
        if "\r\n" in data:
            data_list = data.split("\r\n")
        else:
            data_list = data.split("\n")
        for s in data_list:
            comment_index = s.find("#")
            if comment_index != -1:
                s = s[: comment_index]
            if len(s) == 0: continue
            s = s.replace(" ", "\t")
            tup = tuple(s.split("\t"))
            if (len(tup) != 2): return {}
            temp_tup = []
            for t in tup:
                if t.find('.') == -1: temp_tup.append(int(t))
                else: temp_tup.append(float(t))
            if not dataset.has_key(temp_tup[0]): dataset[temp_tup[0]] = []
            dataset[temp_tup[0]].append(temp_tup[1])
    return dataset
def load_data_vector(filename):
    dataset = {}
    with open(filename, "r") as fp:
        data = fp.readlines()[1:]
        for line in data:
            vec_list = line[:-1].split(' ')
            value = [float(x) for x in vec_list[1:]]
            dataset[int(vec_list[0])] = value
        fp.close()
    return dataset

# 搜索二度和三度人脉
def latent_friends(node, graph):
    links = set(graph.node(node).keys())
    temp_links = set()
    for node in links:
        temp_links = temp_links | set(graph.node(node).keys())
    links = links | temp_links
    return links

def test_precs():
    friends_latent = load_data_set('../data/friends_latent.txt')
    friends = set()
    for link in friends_latent:
        friends.add((link[0], link[1]))
    test = load_data_set('../data/test.txt')
    print len(friends & test)
def preprocessing():
    print 'get the k-degree relationship of nodes'
    g = Graph("../data/train.txt")
    # g = Graph("../data/friends.txt")
    g.read()
    model = Model(g)
    ''' new version '''
    model.find_latent_friends()
if __name__ == '__main__':
    r = load_data_vector('../data/train.embedding')
    print len(r)
    print r[1]