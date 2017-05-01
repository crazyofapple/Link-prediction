#coding=utf-8

from graph import Graph
from utils import evaluate
import math

class Model:
    def __init__(self, graph):
        self.__graph = graph

    def train(self):
        mp = {}
        nodes = self.__graph.all_nodes()
        for ni in nodes:
            linkis = self.__graph.node(ni)
            for nj in nodes:
                if nj <= ni or self.__graph.edge(ni, nj) is not None: continue
                linkjs = self.__graph.node(nj)
                intersect =[x for x in linkis if x in linkjs]
                adar_value = sum([1.0/math.log10(self.__graph.degree(x)) for x in intersect])
                if (math.fabs(adar_value) <= 1e-5): continue;
                mp[(ni,nj)] =  adar_value;
        return dict(sorted(mp.iteritems(), key=lambda x:x[1], reverse=True))

    def predict(self, mp, pred_num=None):
        pred_edges = set()
        cur_num = 0
        for nodes, neighbors in mp.iteritems():
            if pred_num == None:
                pred_edges.add((nodes[0], nodes[1]))
            elif cur_num < pred_num:
                pred_edges.add((nodes[0], nodes[1]))
                cur_num += 1
        with open('../data/result.txt', "w") as fp:
            for pred_edge in pred_edges:
                string = '%d\t%d\n' % (pred_edge[0], pred_edge[1])
                fp.write(string)
            fp.close()
        return pred_edges

def load_data(filename):
    dataset = set()
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
            if len(s) == 0:
                continue
            s = s.replace(" ", "\t")
            node_tuple = tuple(s.split("\t"))
            dataset.add(node_tuple)
    return dataset

if __name__ == '__main__':
    g = Graph("../data/train.txt")
    g.read()
    model = Model(g)
    mp = model.train()
    print len(mp)
    '''
    k = 0
    for i, j in mp.iteritems():
        print i, j
        k += 1
        if k == 11:
            break 
    max1 = -1
    ans = -1
    ansrst = {}
    '''
    #for i in range(12000, 100000):
    result = model.predict(mp, 53903)
    result = load_data('../data/result.txt')
    test = load_data('../data/test.txt')
    rst = evaluate(test, result, quiet=False)
    #    if max1 < rst['F1']:
    #        max1 = rst['F1']
    #        ans = i
    #        ansrst = rst;    
    #print ans
    #print ansrst
