
# coding: utf-8

# In[ ]:


import numpy as np
import warnings
import networkx as nx
import scipy.io
import matplotlib.pyplot as plt
import Classifier
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import scipy.misc
from scipy import io
import os
import numpy as np
import json
import math
# In[2]:



#
# def parse_mat_file(path):
#
#     edges = []
#     g = nx.Graph()
#     #mat = scipy.io.loadmat(path)
#     mat = io.loadmat(path)
#     nodes = mat['network'].tolil()#(0,175) 1.0   (0,282) 1.0 ....对儿
#     subs_coo = mat['group'].tocoo()#(27, 0)	1.0 ...
#
#     for start_node,end_nodes in enumerate(nodes.rows, start=0):
#         for end_node in end_nodes:#end_nodes中保存了第二列的distinct数据
#             edges.append((start_node,end_node))
#
#     g.add_edges_from(edges)
#     g.name = path
#     print(nx.info(g) + "\n---------------------------------------\n")
#
#     return g, subs_coo


# In[3]:


# def load_embeddings(fname):
#     try:
#         word_vec = KeyedVectors.load_word2vec_format(fname, binary=False)
#         print("Embeddings successfully loaded from "+fname)
#         return word_vec, True
#     except IOError:
#         print("Embedding file not found. Proceeding to generate new embeddings")
#         # Y/N here
#         #return _, False
#         return False


# In[4]:


def eval_classifier(G, subs_coo, word_vec):
    #Sometimes the model doesn't predict anything at all for some inputs. Its either the model's fault or that user has no subscriptions at
    #all, in that case the model is predicting properly but of course a zero output would raise exceptions during sklearn's
    #F1 score function.
    #Currently evaluating performance with OVR Logistic Regression.
    print("\t**Evaluating classifier performance with the embeddings**")

    results = Classifier.evaluate(G, subs_coo, word_vec)
    
    print("\n Evaluation completed using the following:")
    for i in results.keys():
        print("--> ",i)
    
    print("\nPrinting evaluation results : ")
    trainsize = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    for (name,res) in results.items():
        print("\n\nClassifier : ",name)
        for (tr_size,res_) in zip(trainsize,res):
            print("\tTraining size : ",tr_size)
            print("\t\tMicro F1: ",res_[0])
            print("\t\tMacro F1: ",res_[1])
        
        avg = np.average(res,axis=0)
        print("\t---------------------------------------")
        print("\t Average Micro F1 : ",avg[0])
        print("\t Average Macro F1 : ",avg[1])
        Classifier.plot_graph(trainsize, res)


# In[5]:


#warnings.filterwarnings("ignore")
#G, subs_coo = parse_mat_file('F:\\(metapath2vec)\\other_code\\node2vec-master\\node2vec-master\\src\\graph\\blogcatalog.mat')

index2nodeid = json.load(open("F:\\(metapath2vec)\\other_code\\metapath2vec-master\\metapath2vec-master\\log宋蕊数据集有类别\\index2nodeid.json"))
index2nodeid = {int(k):v for k,v in index2nodeid.items()}
nodeid2index = {v:int(k) for k,v in index2nodeid.items()}
node_embeddings = np.load("F:\\(metapath2vec)\\other_code\\metapath2vec-master\\metapath2vec-master\\log宋蕊数据集有类别\\node_embeddings.npz")['arr_0']

eval_classifier(G, subs_coo, node_embeddings)

