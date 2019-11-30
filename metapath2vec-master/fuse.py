import numpy as np
import json
import csv
import heapq
from collections import Counter

#读取三个文件的向量
dir = ".\\data\\upu\\recommend"
index2nodeid = json.load(open(dir+"\\log\\index2nodeid.json"))
index2nodeid = {int(k): v for k, v in index2nodeid.items()}
nodeid2index_upu = {v: int(k) for k, v in index2nodeid.items()}
node_embeddings_upu = np.load(dir+"\\log\\node_embeddings.npz")['arr_0']
# 100维的向量

dir = ".\\data\\utp\\recommend"
index2nodeid = json.load(open(dir+"\\log\\index2nodeid.json"))
index2nodeid = {int(k): v for k, v in index2nodeid.items()}
nodeid2index_upcpu = {v: int(k) for k, v in index2nodeid.items()}
node_embeddings_upcpu = np.load(dir+"\\log\\node_embeddings.npz")['arr_0']

dir = ".\\data\\ulp\\recommend"
index2nodeid = json.load(open(dir+"\\log\\index2nodeid.json"))
index2nodeid = {int(k): v for k, v in index2nodeid.items()}
nodeid2index_utlptlu = {v: int(k) for k, v in index2nodeid.items()}
node_embeddings_utlptlu = np.load(dir+"\\log\\node_embeddings.npz")['arr_0']

# 存放poi和user的id
poilist = list()
userlist = list()

#读取用户和poi列表
def readnodetype():
    f = open('.\\data\\upu\\vector\\node_type_mapings.txt', 'r')
    line = f.readline()
    while line:
        list = line.strip().split(" ")
        if (len(list) == 2):
            if (list[1].__eq__("poi")):
                poilist.append(list[0])
            elif (list[1].__eq__("user")):
                userlist.append(list[0])
        line = f.readline()
    f.close()

# 余弦相似度
#计算向量相似性
def cos_sim(vector_a, vector_b):
    """
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a
    :param vector_b: 向量 b
    :return: sim
    """
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim

# 余弦值的范围在[-1,1]之间，值越趋近于1，代表两个向量的方向越接近；
# 越趋近于-1，他们的方向越相反；接近于0，表示两个向量近乎于正交。
def calsim(list,a,b,c):
    #遍历list元素
    readnodetype()
    with open('.\\data\\fuse\\simdict.txt', 'w') as fb:
        # print(len(poilist))
        for i in list:
            for j in list:
                #读取向量
                upu_a = node_embeddings_upu[nodeid2index_upu[i]]
                upu_b = node_embeddings_upu[nodeid2index_upu[j]]
                upcpu_a = node_embeddings_upcpu[nodeid2index_upcpu[i]]
                upcpu_b = node_embeddings_upcpu[nodeid2index_upcpu[j]]
                utlptlu_a = node_embeddings_utlptlu[nodeid2index_utlptlu[i]]
                utlptlu_b = node_embeddings_utlptlu[nodeid2index_utlptlu[j]]
                #按照权重融合向量
                vector_a = a*np.array(upu_a) + b*np.array(upcpu_a) + c*np.array(utlptlu_a)
                vector_b = a*np.array(upu_b) + b*np.array(upcpu_b) + c*np.array(utlptlu_b)

                sim = cos_sim(vector_a, vector_b)
                fb.write(str(i)+"\t"+str(j)+"\t"+str(sim))
                fb.write("\n")
                # print('sim:', sim)
    fb.close()

#找一个id的前k个相似的id
def topk(id,k):
    f = open('.\\data\\fuse\\simdict.txt', 'r', encoding='UTF-8', errors='ignore')
    line = f.readline()
    #提取与poiid有关（可以作为poi1或poi2）的list列表，【poi1，poi2，simi】
    simlist = list()    #存放相似性值
    idlist = list() #存放对应相似性的poi的id
    while line:
        str = line.strip().split("\t")
        if(id == str[0]):
            idlist.append(str[1])
            simlist.append(str[2])
        line = f.readline()
    f.close()
    #找topk相似性的索引
    a = np.array(simlist)
    topid = heapq.nlargest(k, range(len(a)), a.take)
    #根据索引输出相似id以及相似度
    simdict = dict()  #topk的id,sim字典
    toplist = [] #topk的id列表
    for i in topid:
        simdict[idlist[i]] = simlist[i]
        toplist.append(idlist[i])
    return simdict,toplist

##########################################评估指标###########################################
def eval(test,rec):#参数：一个用户u的测试集，推荐列表
    precision = 0
    recall = 0

    if len(rec)!=0:
        intersection = [i for i in test if i in rec] #求交集
        recall = len(intersection) / len(test)

        inter = set(intersection)
        r = set(rec)
        precision = len(inter) / len(r)

    if precision == 0 or recall == 0:
        f1 = 0
    else:
        f1 = 2*precision*recall /(precision+recall)

    return precision,recall,f1

####################################没有输入时间地点的推荐####################################
user_poilist = dict()
#topid:相似用户序列，k返回推荐的poi个数
def recommadation(topid,k):
    user_poilist.clear()
    #推荐列表
    # 1、统计每个用户访问的poi
    with open(".\\data\\upu\\input\\user_poi.txt", 'r', encoding='ISO-8859-1') as pafile:
        for line in pafile:
            toks = line.strip().split("\t")
            if len(toks) == 2:
                u, p = toks[0], toks[1]
                # u:'37',p:'4e3e097552b1a04aff2139ff'
                if u not in user_poilist:
                    user_poilist[u] = []
                user_poilist[u].append(p)

    # 2、拼接这些poi，计算地点出现频率，并从高到低排序
    list = []
    for item in topid:
        list = list + user_poilist[item]
    list.sort()

    # 3、返回topk推荐列表
    counter = Counter(list)
    result = counter.most_common(k)
    rec = []
    for item in result:
        rec.append(item[0])
    return rec

##########################################输入时间地点的推荐####################################
dirtest = '.\\data\\99user'
id_tl = dict()  #tlid,hour
def readtl():
    # 读取时空id
    with open(dirtest + "\\id_tl.txt", 'r', encoding='ISO-8859-1') as cdictfile:
        for line in cdictfile:
            toks = line.strip().split("\t")
            if len(toks) == 2:
                id_tl[toks[0]] = toks[1]  # tl的id，time&loc

def rec_tl(time,loc,topid,k):
    user_poilist.clear()
    # 1、统计每个用户在指定时空邻域内所去的poi
    with open(dirtest + "\\train.txt", 'r', encoding='ISO-8859-1') as pafile:
        for line in pafile:
            toks = line.strip().split("\t")
            if len(toks) == 4:
                u, tl, p = toks[0], toks[1], toks[2]
                if abs(int(id_tl[tl][0:2]) - int(time)) < 4 and str(id_tl[tl][2:]).__eq__(loc):    #在相近的时间范围和相同的区域内
                    if u not in user_poilist:
                        user_poilist[u] = []
                    user_poilist[u].append(p)

    # 2、拼接这些poi，计算地点出现频率，并从高到低排序
    list = []
    for item in topid:
        if user_poilist.__contains__(item):
            list = list + user_poilist[item]
    list.sort()

    # 3、返回topk推荐列表
    counter = Counter(list)
    result = counter.most_common(k)
    rec = []
    for item in result:
        rec.append(item[0])

    #如果相似用户未推荐出序列，则根据相似用户的全部行为习惯来预测
    if len(rec)==0:
        rec = recommadation(topid,k)
    return rec

###########################################读取测试文件###################################
def readtest():
    uptest = dict()   #读取用户签入的poi
    utlptest = dict()   #读取用户在特定时间签入的poi
    #统计每个用户以及所去的poi
    with open(dirtest + "\\test.txt", 'r', encoding='ISO-8859-1') as pafile:
        for line in pafile:
            toks = line.strip().split("\t")
            if len(toks) == 4:
                u, tl, p = toks[0], toks[1],toks[2]
                if u not in uptest:
                    uptest[u] = []
                uptest[u].append(p)
                utl = u+"-"+tl
                if utl not in utlptest:
                    utlptest[utl] = []
                utlptest[utl].append(p)
    return uptest,utlptest

if __name__ == "__main__":

    calsim(userlist,1,1,1) #统计user相似
    uptest, utlptest = readtest()  #读取测试集

    topkuser = 3  # 相似用户个数
    allk = [5,10,20,30,50]#推荐列表


    for k in allk:

        print("k值："+str(k))
        #不输入时间的评估
        sumpre = 0
        sumrecall = 0
        sumf1 = 0
        for userid in uptest:
            topdict,topid = topk(userid,topkuser)  #获取topk个相似用户
            #获取相似user的推荐列表
            rec = recommadation(topid,k)
            test = uptest[userid]
            #评估
            precision,recall,f1 = eval(test,rec)
            sumpre = sumpre + precision
            sumrecall = sumrecall + recall
            sumf1 = sumf1 + f1
        print('只输入用户的评估：')
        print("precision:" + str(sumpre / len(uptest)))
        print("recall:" + str(sumrecall / len(uptest)))
        print("f1:" + str(sumf1 / len(uptest)))

        # #输入时空的评估
        # sumpre = 0
        # sumrecall = 0
        # sumf1 = 0
        # readtl()
        # for utlp in utlptest:
        #     temp = utlp.split('-')
        #     userid = temp[0]
        #     time = id_tl[temp[1]][0:2]
        #     loc = id_tl[temp[1]][2:]
        #
        #     topdict,topid = topk(userid,topkuser)  #获取topk个相似用户
        #     rec = rec_tl(time,loc,topid,k)  #获取相似user的相似时间的推荐poi列表
        #     test = utlptest[utlp]
        #     #评估
        #     precision,recall,f1 = eval(test,rec)
        #     sumpre = sumpre + precision
        #     sumrecall = sumrecall + recall
        #     sumf1 = sumf1 + f1
        # print('输入用户、时间、地点的评估：')
        # print("precision:"+ str(sumpre/len(utlptest)))
        # print("recall:" + str(sumrecall / len(utlptest)))
        # print("f1:" + str(sumf1 / len(utlptest)))
        # print('\n')