import numpy as np
import json
import csv

# 路径要改！！！！！！！！！！！！！！！
dir = ".\\data\\pup\\recommend\\log"

index2nodeid = json.load(open(dir +"\\index2nodeid.json"))
index2nodeid = {int(k): v for k, v in index2nodeid.items()}
nodeid2index = {v: int(k) for k, v in index2nodeid.items()}
node_embeddings = np.load(dir +"\\node_embeddings.npz")['arr_0']
# 100维的向量
# 存放poi和user的id
poilist = list()
userlist = list()
poi_cate = dict()


# 路径要改！！！！！！！！！！！！！！！
dirpath = ".\\data\\pup\\vector"
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


def poi_category():
    f = open(dirpath+"\\poi_cate_index.txt", 'r')
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
def testsimi():
    det_a = node_embeddings[nodeid2index["37"]]
    det_b = node_embeddings[nodeid2index["1085"]]
    print(det_a)
    print(det_b)
    vector_a, vector_b = np.array(det_a), np.array(det_b)
    similirity2 = cos_sim(vector_a, vector_b)
    print('similirity2:', similirity2)


data2csv()
