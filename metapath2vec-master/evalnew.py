from gensim.models import KeyedVectors
import numpy as np


dirpath = ".\\data\\Foursquare\\output"
word2vec_dict = dict()
pois = dict()
users = dict()
tls = dict()
def readvector():
    d = 100
    numwalks = 20  # 同一个起点开始的路径的数量
    walklength = 10  # 路径长度

    path = dirpath + '\\d' + str(d) + '-walk_length' + str(walklength) + '-num_walks' + str(numwalks)+ '.vector'
    model = KeyedVectors.load_word2vec_format(path)
    word2vec_dict = dict()
    for word, vector in zip(model.vocab, model.vectors):
        if '.bin' not in path:
            word2vec_dict[word] = vector
        else:
            word2vec_dict[word] = vector / np.linalg.norm(vector)

    for each in word2vec_dict:
        if str(each).startswith('u'):
            users[each] = word2vec_dict[each]
        elif str(each).startswith('p'):
            pois[each] = word2vec_dict[each]
        elif str(each).startswith('tl'):
            tls[each] = word2vec_dict[each]

    return word2vec_dict, pois
    #     print(each, word2vec_dict[each])

def readtest():
    utl_p = dict()
    with open(".\\data\\Foursquare\\train2id.txt", 'r', encoding='ISO-8859-1') as adictfile:
        for line in adictfile:
            toks = line.strip().split("\t")
            if len(toks) == 3:
                u, p, tl = toks[0], toks[1], toks[2]
                if (u, tl) not in utl_p:
                    utl_p[(u, tl)] = []
                utl_p[(u, tl)].append(p)
    return  utl_p

def calscore(u,tl):
    p_score = dict()
    if (u not in word2vec_dict) or (tl not in word2vec_dict):
        return 0
    else:
        for p in pois:
            uv = word2vec_dict[u]
            pv = pois[p]
            tlv = word2vec_dict[tl]
            score = np.dot(uv,pv)+np.dot(tlv,pv)
            p_score[p] = score
    p_score = sorted(p_score.items(), key=lambda x: x[1], reverse=True)

    return p_score
##########################################评估指标###########################################
def eval(tru,pre):#参数：一个用户u的POI真实集，测试集
    precision = 0
    recall = 0

    if len(pre)!=0:
        intersection = [i for i in tru if i in pre] #求交集
        inter = set(intersection)

        recall = len(inter) / len(tru)
        precision = len(inter) / len(pre)

    if precision == 0 or recall == 0:
        f1 = 0
    else:
        f1 = 2*precision*recall /(precision+recall)

    return precision,recall,f1

if __name__ == "__main__":

    word2vec_dict,pois = readvector()
    p_score = calscore('u8','tl142')
    utl_p = readtest()
    k = 5
    pre = []
    tru = utl_p[('8','142')]
    for i in range(k):
        poi = p_score[i][0]
        pre.append(poi)

    print(set(tru))
    print(set(pre))