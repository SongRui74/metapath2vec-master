import numpy as np
import json
import csv
import heapq
from collections import Counter

dir = ".\\data\\upu\\recommend"
index2nodeid = json.load(open(dir+"\\log\\index2nodeid.json"))
index2nodeid = {int(k): v for k, v in index2nodeid.items()}
nodeid2index = {v: int(k) for k, v in index2nodeid.items()}
node_embeddings = np.load(dir+"\\log\\node_embeddings.npz")['arr_0']
# 100维的向量

# 存放poi和user的id
poilist = list()
userlist = list()
dirpath = ".\\data\\upu\\vector"
#读取用户和poi列表
def readnodetype():
    f = open(dirpath+'\\node_type_mapings.txt', 'r')
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

# poi_cate = dict()
# def poi_category():
#     f = open(dirpath+"\\poi_cate_index.txt", 'r')
#     line = f.readline()
#     while line:
#         list = line.strip().split("\t")
#         if (len(list) == 2):
#             if (list[0] not in poi_cate):
#                 poi_cate[list[0]] = list[1]
#         line = f.readline()
#     f.close()
#
# def data2csv():
#     readnodetype()  # 构造poilist
#     # print(poilist)
#     poi_category()  # 构造poi_cate字典
#     # print(poi_cate)
#     with open(dirpath+"\\vector.csv", "w") as csvfile:
#         writer = csv.writer(csvfile)
#         # 先写入columns_name # 写入多行用writerows
#         row = []
#         row.append('index')
#         for i in range(0, 100):
#             row.append('n' + str(i))
#         row.append('category')
#         writer.writerow(row)
#
#         for poi in poilist:
#             cate = poi_cate[poi]
#             vec = np.array(node_embeddings[nodeid2index[poi]])
#             temp = []
#             temp.append(poi)
#             for i in range(0, len(vec)):
#                 temp.append(vec[i])
#             temp.append(cate)
#             writer.writerow(temp)

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
def calsim(list):
    #遍历poi元素
    readnodetype()  # 构造poilist
    # print(poilist)
    #poi1 \t poi2\t simi的格式写入txt
    with open(dir+'\\simdict.txt', 'w') as fb:
        # print(len(poilist))
        for i in list:
            for j in list:
                det_a = node_embeddings[nodeid2index[i]]
                det_b = node_embeddings[nodeid2index[j]]
                # print(det_a)
                # print(det_b)
                vector_a, vector_b = np.array(det_a), np.array(det_b)
                sim = cos_sim(vector_a, vector_b)
                fb.write(str(i)+"\t"+str(j)+"\t"+str(sim))
                fb.write("\n")
                # print('sim:', sim)
    fb.close()

#找一个id的前k个相似的id
def topk(id,k):
    #读文件，list列表，【poi1，poi2，simi】
    f = open(dir+'\\simdict.txt', 'r', encoding='UTF-8', errors='ignore')
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
    intersection = [i for i in test if i in rec] #求交集

    precision = len(intersection) / len(rec)
    recall = len(intersection) / len(test)
    if precision == 0  or recall == 0:
        f1 = 0
    else:
        f1 = 2*precision*recall /(precision+recall)

    return precision,recall,f1

####################################没有输入时间地点的推荐####################################
user_poilist = dict()
dirrec = '.\\data\\upu\\input'
#topid:相似用户序列，k返回推荐的poi个数
def recommadation(topid,k):
    #推荐列表
    # 1、统计每个用户访问的poi
    with open(dirrec + "\\user_poi.txt", 'r', encoding='ISO-8859-1') as pafile:
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

##########################################输入时间的推荐####################################
dirtest = '.\\data\\100user'
id_tl = dict()  #tlid,hour
def rec_tl(time,topid,k):
    user_poilist.clear()
    #读取时空id
    with open(dirtest + "\\id_tl.txt", 'r', encoding='ISO-8859-1') as cdictfile:
        for line in cdictfile:
            toks = line.strip().split("\t")
            if len(toks) == 2:
                id_tl[toks[0]] = toks[1][0:2]  # tl的id，time

    # 1、统计每个用户在指定时间邻域内所去的poi
    with open(dirtest + "\\train.txt", 'r', encoding='ISO-8859-1') as pafile:
        for line in pafile:
            toks = line.strip().split("\t")
            if len(toks) == 4:
                u, tl, p = toks[0], toks[1], toks[2]
                if abs(int(id_tl[tl]) - int(time)) < 4:    #在相近的时间范围内
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

    # data2csv()  # id向量类别信息写入csv文件 可以用weka进行聚类分类

    calsim(userlist) #统计user相似
    uptest, utlptest = readtest()  #读取测试集

    sumpre = 0
    sumrecall = 0
    sumf1 = 0

    #不输入时间的评估
    for userid in uptest:
        topdict,topid = topk(userid,30)  #获取topk个相似用户
        #获取相似user的推荐列表
        rec = recommadation(topid,50)
        test = uptest[userid]
        #评估
        precision,recall,f1 = eval(test,rec)
        sumpre = sumpre + precision
        sumrecall = sumrecall + recall
        sumf1 = sumf1 + f1
    print("precision:" + str(sumpre / len(uptest)))
    print("recall:" + str(sumrecall / len(uptest)))
    print("f1:" + str(sumf1 / len(uptest)))

    #输入时间的评估
    # for utlp in utlptest:
    #     temp = utlp.split('-')
    #     userid = temp[0]
    #     time = id_tl[temp[1]]
    #
    #     topdict,topid = topk(userid,10)  #获取topk个相似用户
    #     rec = rec_tl(time,topid,50)  #获取相似user的相似时间的推荐poi列表
    #     test = utlptest[utlp]
    #     #评估
    #     precision,recall,f1 = eval(test,rec)
    #     sumpre = sumpre + precision
    #     sumrecall = sumrecall + recall
    #     sumf1 = sumf1 + f1
    # print("precision:"+ str(sumpre/len(uptest)))
    # print("recall:" + str(sumrecall / len(uptest)))
    # print("f1:" + str(sumf1 / len(uptest)))