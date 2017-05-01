#encoding:utf-8
from __future__ import division
from utils import evaluate
from graph import Graph
from radio import start_ratio
from preprocess import preprocessing, load_data_list,load_data_set, load_data_dict, test_precs, load_data_vector
import math
from scipy.spatial import distance
import numpy as np
import networkx as nx

def common_friends(graph, node_a, node_b):
    friends_a = set(graph.node(node_a).keys())
    friends_b = set(graph.node(node_b).keys())
    return (friends_a & friends_b)
#节点i与其K度人脉j的公共朋友数
def test_CN():
    g = Graph("../data/train.txt")
    g.read()
    test = load_data_list("../data/friends_latent.txt")
    with open('../data/test_result.txt', 'w') as fp:
        for t in test:
            fp.write('%d\t%d\t%d\n' % (t[0], t[1], len(common_friends(g, t[0], t[1]))))
        fp.close()
#节点i与其K度人脉j的jaccard权值 
def test_JA():
    g = Graph("../data/train.txt")
    g.read()
    test = load_data_list("../data/friends_latent.txt")
    with open('../data/test_result2.txt', 'w') as fp:
        for t in test:
            friends_a = set(g.node(t[0]).keys())
            friends_b = set(g.node(t[1]).keys())
            cmn_friends = friends_a & friends_b
            jaccard = len(cmn_friends) / (len(friends_a) + len(friends_b) - len(cmn_friends))
            fp.write('%d\t%d\t%f\n' % (t[0], t[1], jaccard))
        fp.close()
#节点i与其K度人脉j的RA权值 
def test_RA():
    g = Graph("../data/train.txt")
    g.read()
    test = load_data_list("../data/friends_latent.txt")
    with open('../data/test_result3.txt', 'w') as fp:
        for t in test:
            cmn_friends = common_friends(g, t[0], t[1])
            adamic_coef = 0.0
            for node in cmn_friends:
                adamic_coef += 1.0 / math.pow(len(g.node(node)), 1.0)
            fp.write('%d\t%d\t%f\n' % (t[0], t[1], adamic_coef))
        fp.close()
#节点i与其K度人脉j的Preferential attacchment权值 
def test_PA():
    g = Graph("../data/train.txt")
    g.read()
    test = load_data_list("../data/friends_latent.txt")
    with open('../data/test_result4.txt', 'w') as fp:
        for t in test:
            friends_a = set(g.node(t[0]).keys())
            friends_b = set(g.node(t[1]).keys())
            fp.write('%d\t%d\t%d\n' % (t[0], t[1], len(friends_a) * len(friends_b)))
        fp.close()
def test_Deepwalk():
    g = Graph("../data/train.txt")
    g.read()
    test = load_data_list("../data/friends_latent.txt")
    vector = load_data_vector("../data/friends.embedding")
    with open('../data/test_result5.txt', 'w') as fp:
        for t in test:
            friends_a = vector[t[0]]
            friends_b = vector[t[1]]
            fp.write('%d\t%d\t%d\n' % (t[0], t[1],  np.dot(friends_a, friends_b)))
        fp.close()
def test_Katz():
    g = Graph("../data/train.txt")
    g.read()
    train = load_data_dict("../data/train.txt")
    G = list(train.values())
    dim = len(G)
    mat = np.zeros((dim, dim), dtype = np.int)
    for i in range(dim):
        for j in G[i]:
            mat[i][j] = 1
    beta = 0.8
    sim = np.linalg.inv(np.eye(dim) - beta * mat) - np.eye(dim)
    test = load_data_list("../data/friends_latent.txt")
    with open('../data/test_result6.txt', 'w') as fp:
        for t in test:
            fp.write('%d\t%d\t%d\n' % (t[0], t[1],  sim[t[0]][t[1]]))
        fp.close()
def test_ra_ISH():
    G = nx.Graph()
    G.add_edges_from(np.loadtxt('../data/train.txt',dtype=int))
    for n in G.nodes():
        G.node[n]['community'] = 0
    test = np.loadtxt('../data/friends_latent.txt',dtype=int)
    preds = nx.ra_index_soundarajan_hopcroft(G, test[:,0:2])
    with open('../data/result_RA_ISH.txt','w') as f:
        for u, v, p in preds:
            f.write('%d\t%d\t%f\n' % (u,v,p))

#test_WICluster
def test_WICluster():
    G = nx.Graph()
    G.add_edges_from(np.loadtxt('../data/train.txt',dtype=int))
    for n in G.nodes():
        G.node[n]['community'] = 0
    test = np.loadtxt('../data/friends_latent.txt',dtype=int)
    preds = nx.within_inter_cluster(G, test[:,0:2])
    with open('../data/result_WICluster.txt','w') as f:
        for u, v, p in preds:
            f.write('%d\t%d\t%f\n' % (u,v,p))    
def normalize(link_scores):
    if not link_scores: return {}
    max_score = max(link_scores.values())
    min_score = min(link_scores.values())
    mean = np.mean(link_scores.values())
    std = np.std(link_scores.values())
    sum_score = sum(link_scores.values())
    
    if (max_score == min_score):
        max_score = 1.0
        min_score = 0.0
    if abs(max_score) <= 1e-7: max_score = 1.0
    if abs(sum_score) <= 1e-7: sum_score = 1.0
    p = 1e-5
    for link, score in link_scores.iteritems():
        link_scores[link] = (score - min_score) / (max_score - min_score)
    return link_scores


def ensemble(rate=1.0, number=None):
    trainset = load_data_dict('../data/train.txt')
    ratios = load_data_dict('../data/ratio.txt') # ratio that testset / trainset
    link_scores = {}
    filenames = (('../data/test_result5.txt', 0.3),('../data/test_result2.txt', 0.2), ('../data/test_result3.txt', 0.3), ('../data/test_result4.txt', 0.2),)
    #filenames = (('../data/test_result5.txt', 0.3),('../data/test_result2.txt', 0.2),
    # ('../data/result_RA_ISH.txt', 0.3), ('../data/test_result4.txt', 0.1), ('../data/test_result6.txt', 0.1), ('../data/result_WICluster.txt', 0.3))
    for filename, weight in filenames:
        result = load_data_list(filename)
        temp_scores = {}
        node = 0
        for ni, nj, score in result:
            if ni == node:
                temp_scores[(ni, nj)] = score
            else:
                for link, score in normalize(temp_scores).iteritems():
                    if not link_scores.has_key(link[0]): link_scores[link[0]] = {}
                    if not link_scores[link[0]].has_key(link[1]): link_scores[link[0]][link[1]] = 0
                    #if abs(score) <= 0.1: score = 0
                    link_scores[link[0]][link[1]] += weight * abs(score)
                node = ni
                temp_scores = {}
                temp_scores[(ni, nj)] = score
    with open('../data/ensemble_result.txt', 'w') as fp:
        result_set = set()
        total_count = 0
        temp_dict = {}
        for ni, temp_scores in link_scores.iteritems():
            #if abs(ratios[ni][0]) <= 1e-5: continue
            count = int(math.ceil(rate * max(0.0, min(ratios[ni][0],0.6)) * len(trainset[ni]))) 
            #if len(trainset[ni]) == 1:
            #    count = min(0, count)
            #count = int((1.0 * len(trainset[ni]) / 9.0))
            temp_scores = dict(sorted(temp_scores.iteritems(), key=lambda x:x[1], reverse=True)[0:count])
            for nj, score in temp_scores.iteritems():
                if (ni,nj) in result_set: continue
                #if abs(score) <= 0.1: continue
                fp.write('%d\t%d\n' % (ni, nj))
                #fp.write('%d\t%d\n' % (nj, ni))
                temp_dict[(ni, nj)] = score
                result_set.add((ni,nj))
                result_set.add((nj,ni))
                total_count += 1
        print 'total_count:', total_count
        #temp_dict = dict(sorted(temp_dict.iteritems(), key=lambda x:x[1], reverse=True)[0:int(total_count)])
        #for pair, score in temp_dict.iteritems():
        #    fp.write('%d\t%d\n' % (pair[0], pair[1]))
        fp.close()


if __name__ == '__main__':
    #start_ratio(count=10000)
    #preprocessing()
    
    print 'using ensemble method for link prediction.'
    #test_precs()
    #test_CN()
    #test_JA()
    #test_RA()
    #test_PA()
    #test_Deepwalk()
    #test_Katz()
    #test_WICluster()
    #test_ra_ISH()
    ensemble()
    result = load_data_set('../data/ensemble_result.txt')
    test = load_data_set('../data/test.txt')
    rst = evaluate(test, result)
    #train = load_data_set(u'../data/16S051078_ldf_ensemble_result_1.txt')
    #test = load_data_set(u'../data/result_ans.txt')
    #rst = evaluate(test, train)
       
    

