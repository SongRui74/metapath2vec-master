#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Satoshi Tsutsui <stsutsui@indiana.edu>
class to get the data in a batch way
includes the sampler for word2vec negative sampling
'''


import numpy as np
import random
# import scipy
import os

class Dataset(object):
    def __init__(self,random_walk_txt,node_type_mapping_txt,window_size):
        index2token,token2index,word_and_counts,index2frequency,node_context_pairs= self.parse_random_walk_txt(random_walk_txt,window_size)
        self.window_size = window_size
        self.nodeid2index = token2index
        self.index2nodeid = index2token
        self.index2frequency = index2frequency
        index2type,type2indices = self.parse_node_type_mapping_txt(node_type_mapping_txt, self.nodeid2index)
        self.index2type = index2type
        self.type2indices = type2indices
        self.node_context_pairs= node_context_pairs
        self.prepare_sampling_dist(index2frequency,index2type,type2indices)
        self.shffule()
        self.count = 0
        self.epoch = 1

    def parse_node_type_mapping_txt(self,node_type_mapping_txt,nodeid2index):
        #this method does not modify any class variables
        index2type={}
        
        with open(node_type_mapping_txt) as f:
            for line in f: #‘i pronoun\n’
                pair = [entry for entry in line.strip().split(' ')]#['i','pronoun']
                if len(pair[0])==0 or len(pair[1])==0:
                    print("something is wrong!!!")
                    print(pair)
                    continue
                index2type[nodeid2index[pair[0]]]=pair[1]
                #index2type[0:'pronoun']原始单词的id对应的type
        type2indices = {}
        all_types = set(index2type.values())#所有的distinct类型（词性，姓名）
        for node_type in all_types:
            type2indices[node_type]=[]#字典，{‘article:[]’,'verb':[]}

        for node_index,node_type in index2type.items():
            type2indices[node_type].append(node_index)
            #{'article':[9],'verb':[1,4,6,8]}

        #make array because it will be used with numpy later
        for node_type in all_types:
            type2indices[node_type]=np.array(type2indices[node_type])
        #将'verb':[1,4,6,8]中的[]转化为numpy
        return index2type,type2indices

    def parse_random_walk_txt(self,random_walk_txt,window_size):
        #this method does not modify any class variables
        #this will NOT make any <UKN> so don't use for NLP.
        word_and_counts = {}#{'i':2,'love':1,'yi':1,'li':1,......}单词出现的频数map对应
        with open(random_walk_txt) as f:
            for line in f:
                sent = [word.strip() for word in line.strip().split(' ')] #['i','love','yi','li']
                for word in sent:       
                    if len(word) == 0:
                        continue
                    if word in word_and_counts.keys():
                        #.has_key(word)
                        word_and_counts[word] += 1
                    else:
                        word_and_counts[word] = 1


        print("The number of unique words:%d"%len(word_and_counts))
        index2token = dict((i, word) for i, word in enumerate(word_and_counts.keys()) )#enumerate用于组成索引序列，将word_and_counts.keys为单词进行distinct编号
        #index2token为[0:'i',1:'love',.....]
        token2index = dict((v, k) for k, v in index2token.items())
        #token2index为['i':0,'love':1,....]    dict.items返回字典内部的所有数据，key返回键，value返回值。
        index2frequency = dict((token2index[word],freq) for word,freq in word_and_counts.items() )
        #index2frequency{0:2,1:1,2:2.....}返回单词id对应的频数   token2index[word]返回字典中word对应的tokenid。
        #word_word=scipy.sparse.lil_matrix((len(token2index), len(token2index)), dtype=np.int32)
        node_context_pairs = []#let's use naive way now

        print("window size %d"%window_size)

        with open(random_walk_txt) as f:
            for line in f:
                sent = [token2index[word.strip()] for word in line.split(' ') if word.strip() in token2index]
                #sent=[0,1,2,3]对应i love yi li.把句子进行数值化
                sent_length=len(sent)#sent的长度=句子的长度
                for target_word_position,target_word_idx in enumerate(sent):
                    #target_word_position,target_word_idx代表sent序列化之后的值，
                    start=max(0,target_word_position-window_size) #start为目标单词-窗口，即目标单词的前后窗口大小数据
                    end=min(sent_length,target_word_position+window_size+1)
                    context=sent[start:target_word_position]+sent[target_word_position+1:end+1]#context=[1,2]
                    for contex_word_idx in context:
                        node_context_pairs.append((target_word_idx,contex_word_idx))
                        #pair=[(0,1),(0,2),(1,0),(1,2),(1,3),(2,1),(2,3),(3,2)]
                        #word_word[target_word_idx,contex_word_idx]+=1

        #word_word=word_word.tocsr()
        return index2token,token2index,word_and_counts,index2frequency,node_context_pairs

    def get_one_batch(self):
        if self.count == len(self.node_context_pairs):#42
            self.count=0
            self.epoch+=1
        node_context_pair = self.node_context_pairs[self.count]
        self.count+=1
        return node_context_pair

    def get_batch(self,batch_size):
        pairs = np.array([self.get_one_batch() for i in range(batch_size)])
        return pairs[:,0],pairs[:,1]

    def shffule(self):
        random.shuffle(self.node_context_pairs)

    def get_negative_samples(self,pos_index,num_negatives,care_type):
        # if care_type is True it's a heterogeneous negative sampling
        #same output format as https://www.tensorflow.org/api_docs/python/tf/nn/log_uniform_candidate_sampler
        pos_prob = self.sampling_prob[pos_index] 
        if not care_type:
            negative_samples = np.random.choice(len(self.index2nodeid),size=num_negatives,replace=False,p=self.sampling_prob)
            negative_probs = self.sampling_prob[negative_samples]
        else:
            node_type = self.index2type[pos_index]
            sampling_probs = self.type2probs[node_type]
            sampling_candidates = self.type2indices[node_type]
            negative_samples_indices = np.random.choice(len(sampling_candidates),size=num_negatives,replace=True,p=sampling_probs)
            ## 参数意思分别 是从a 中以概率P，随机选择3个, p没有指定的时候相当于是一致的分布
            #a1= np.random.choice(a=5, size=3, replace=False, p=None)
            #replacement 代表的意思是抽样之后还放不放回去，如果是False的话，那么出来的三个数都不一样，如果是
            #True的话， 有可能会出现重复的，因为前面的抽的放回去了。
            negative_samples = sampling_candidates[negative_samples_indices]
            negative_probs = sampling_probs[negative_samples_indices]

        # print(negative_samples,pos_prob,negative_probs)
        return negative_samples,pos_prob.reshape((-1,1)),negative_probs

    def prepare_sampling_dist(self,index2frequency,index2type,type2indices):
        sampling_prob = np.zeros(len(index2frequency))#14列1行的向量。存储的是distinct单词的词频。
        for i in range(len(index2frequency)):
            sampling_prob[i]=index2frequency[i]
        sampling_prob = sampling_prob**(3.0/4.0) #from http://mccormickml.com/2017/01/11/word2vec-tutorial-part-2-negative-sampling/

        #normalize the distributions
        #for caring type
        all_types = set(index2type.values())
        type2probs = {}
        for node_type in all_types:
            indicies_for_a_type = type2indices[node_type]#[2 3 7]
            type2probs[node_type] = np.array(sampling_prob[indicies_for_a_type])#{'name':([1.68,1.68,1....为'name'这个类型的word[2,3,7],对应的类型的prob])}
            type2probs[node_type] = type2probs[node_type]/np.sum(type2probs[node_type])
            #type2probs{'name':([0.38 0.38 0.22]),'noun':([0.5,0.5])....}

        #if not careing type
        sampling_prob = sampling_prob/np.sum(sampling_prob)

        self.sampling_prob = sampling_prob
        self.type2probs = type2probs

if __name__ == '__main__':
    #test code  
    dataset=Dataset(random_walk_txt="../data/test_data/random_walks.txt",node_type_mapping_txt="../data/test_data/node_type_mapings.txt",window_size=1)
    print(dataset.get_batch(2))
    center,context = dataset.get_one_batch()
    print(dataset.sampling_prob)
    print(dataset.get_negative_samples(context,num_negatives=5,care_type=False))
    print(dataset.get_negative_samples(context,num_negatives=2,care_type=True))
