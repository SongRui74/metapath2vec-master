import numpy as np
import json
import csv
import heapq

index2nodeid = json.load(open(".\\log\\index2nodeid.json"))
index2nodeid = {int(k): v for k, v in index2nodeid.items()}
nodeid2index = {v: int(k) for k, v in index2nodeid.items()}
node_embeddings = np.load(".\\log\\node_embeddings.npz")['arr_0']
# 100维的向量

# 存放poi和user的id
poilist = list()
userlist = list()

poi_cate = dict()


def readnodetype():
    f = open('.\\data\\pup\\vector\\node_type_mapings.txt', 'r')
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


def poi_category():
    f = open(".\\data\\pup\\vector\\poi_cate_index.txt", 'r')
    line = f.readline()
    while line:
        list = line.strip().split("\t")
        if (len(list) == 2):
            if (list[0] not in poi_cate):
                poi_cate[list[0]] = list[1]
        line = f.readline()
    f.close()


def data2csv():
    readnodetype()  # 构造poilist
    # print(poilist)
    poi_category()  # 构造poi_cate字典
    # print(poi_cate)
    with open(".\\data\\pup\\vector\\vector.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name # 写入多行用writerows
        row = []
        row.append('index')
        for i in range(0, 100):
            row.append('n' + str(i))
        row.append('category')
        writer.writerow(row)

        for poi in poilist:
            cate = poi_cate[poi]
            vec = np.array(node_embeddings[nodeid2index[poi]])
            temp = []
            temp.append(poi)
            for i in range(0, len(vec)):
                temp.append(vec[i])
            temp.append(cate)
            writer.writerow(temp)


# 欧式距离
# det_a=node_embeddings[nodeid2index["37"]]
# det_b=node_embeddings[nodeid2index["1085"]]
# print(det_a)
# print(det_b)
# npvec1, npvec2 = np.array(det_a), np.array(det_b)
# similirity=math.sqrt(((npvec1 - npvec2) ** 2).sum())
# print('similirity:',similirity)
#
# 余弦相似度
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
def calsim():
    #遍历poi元素
    readnodetype()  # 构造poilist
    # print(poilist)
    #poi1 \t poi2\t simi的格式写入txt
    with open('.\\data\\pup\\recommend\\simdict.txt', 'w') as fb:
        # print(len(poilist))
        for i in poilist:
            for j in poilist:
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

def topk(poiid,k):
    #读文件，list列表，【poi1，poi2，simi】
    f = open('.\\data\\pup\\recommend\\simdict.txt', 'r', encoding='UTF-8', errors='ignore')
    line = f.readline()
    #提取与poiid有关（可以作为poi1或poi2）的list列表，【poi1，poi2，simi】
    simlist = list()    #存放相似性值
    idlist = list() #存放对应相似性的poi的id
    while line:
        str = line.strip().split("\t")
        if(poiid == str[0]):
            idlist.append(str[1])
            simlist.append(str[2])
        line = f.readline()
    f.close()
    #找topk相似性的索引
    a = np.array(simlist)
    topid = heapq.nlargest(k, range(len(a)), a.take)
    #根据索引输出相似id以及相似度
    simdict = dict()
    for i in topid:
        simdict[idlist[i]] = simlist[i]
    return simdict

if __name__ == "__main__":

    # data2csv()  # id向量类别信息写入csv文件
    calsim() #统计poi相似度
    sim = topk('4c040721f56c2d7faaae1d66',3)
    print(sim)

