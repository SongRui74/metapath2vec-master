import numpy as np
import pylab
import matplotlib.pyplot as plt
import random
######################计算poi之间的相似度并存入文件#########################
X = dict()
poi = list()
def read_des():
    data = '.\\data\\uppu\\pd.txt'
    f = open(data, 'r', encoding='UTF-8', errors='ignore')
    line = f.readline()
    while line:
        temp = line.split('\t')
        X[temp[0]] = temp[1]
        poi.append(temp[0])
        line = f.readline() #6482条
# 余弦相似度
def cos_sim(vector_a, vector_b):
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim
def calsim():
    #poi1 \t poi2\t simi的格式写入txt
    with open('.\\data\\uppu\\simdict.txt', 'w') as fb:
        for i in poi:
            for j in poi:
                vector_a = X.get(i)
                vector_b = X.get(j)
                sim = cos_sim(vector_a, vector_b)
                fb.write(str(i)+"\t"+str(j)+"\t"+str(sim))
                fb.write("\n")
                # print('sim:', sim)
    fb.close()
# read_des()
# calsim()

##########################查看相似度分布情况##################################
 #相似度区间[0，1]间隔0.1个数统计：0 0 0 0 0 0 3542 389770 5124698 36485351  总数：42003361
 #相似度区间[0.9，1]间隔0.01个数统计：1481182 1878726 2283776 2737104 3481040 4190478 4933406 5622536 6078738 3798365
# 相似度大于0.98的数据占比 24%
def simi():
    data = '.\\data\\uppu\\simdict.txt'
    f = open(data, 'r', encoding='UTF-8', errors='ignore')
    line = f.readline()
    a1=a2=a3=a4=a5=a6=a7=a8=a9=a10=0
    while line:
        temp = line.split('\t')
        if float(temp[2]) > 0.9 and float(temp[2]) <= 0.91:
            a1 = a1 +1
        elif float(temp[2]) > 0.91 and float(temp[2]) <= 0.92:
            a2 = a2 +1
        elif float(temp[2]) > 0.92 and float(temp[2]) <= 0.93:
            a3 = a3 +1
        elif float(temp[2]) > 0.93 and float(temp[2]) <= 0.94:
            a4 = a4 +1
        elif float(temp[2]) > 0.94 and float(temp[2]) <= 0.95:
            a5 = a5 +1
        elif float(temp[2]) > 0.95 and float(temp[2]) <= 0.96:
            a6 = a6 +1
        elif float(temp[2]) > 0.96 and float(temp[2]) <= 0.97:
            a7 = a7 +1
        elif float(temp[2]) > 0.97 and float(temp[2]) <= 0.98:
            a8 = a8 +1
        elif float(temp[2]) > 0.98 and float(temp[2]) <= 0.99:
            a9 = a9 +1
        elif float(temp[2]) > 0.99 and float(temp[2]) <= 1:
            a10 = a10 +1
        line = f.readline() #6482条

    print(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10)

# print(1481182 / 36485351, 1878726 / 36485351, 2283776 / 36485351, 2737104 / 36485351, 3481040 / 36485351,
#       4190478 / 36485351, 4933406 / 36485351, 5622536 / 36485351, 6078738 / 36485351, 3798365 / 36485351, )

##########################将符合阈值的数据写入新文件##################################
def pp():
    data = '.\\data\\uppu\\simdict.txt'
    f = open(data, 'r', encoding='UTF-8', errors='ignore')
    line = f.readline()
    with open('.\\data\\uppu\\newsimi.txt', 'w') as fb:
        while line:
            temp = line.split('\t')
            if float(temp[2]) >= 0.98:
                #poi1 \t poi2\t simi的格式写入txt
                fb.write(line)
                fb.write("\n")
                # print('sim:', sim)
            line = f.readline()
    fb.close()
# pp()

##############计算相似度的时候代码不好有重复，去重（AB与BA的相似度一样写了两次）##################################
def quchong():
    data = '.\\data\\uppu\\newsimi.txt'
    f = open(data, 'r', encoding='UTF-8', errors='ignore')
    line = f.readline()
    poisimi = dict()
    while line:
        temp = line.split('\t')
        if len(temp)==3:
            p = temp[0]+' '+temp[1]
            p1 = temp[1]+' '+temp[0]
            sim = temp[2]
            if p not in poisimi:
                if p1 not in poisimi:
                    poisimi[p] = sim
        line = f.readline()

    with open('.\\data\\uppu\\finalsimi.txt', 'w') as fb:
        for (k, v) in poisimi.items():
            kk = k.split(' ')
            fb.write(str(kk[0])+"\t"+str(kk[1])+"\t"+str(v))
    fb.close()

# quchong()

##############根据相似度写P-P文件##################################
def p_p():
    ppid = dict()
    data = '.\\data\\uppu\\input\\oldid_newid.txt'
    f = open(data, 'r',errors='ignore')
    line = f.readline()
    while line:
        temp = line.split('\t')
        if len(temp) == 2:
            p1 = str(temp[0])
            p2 = str(temp[1])
            ppid[p1] = p2
        line = f.readline()

    fa = open('.\\data\\uppu\\simi.txt', 'r', encoding='UTF-8', errors='ignore')
    l = fa.readline()
    with open('.\\data\\uppu\\input\\poi_poi.txt', 'w') as fb:
        while l:
            temp = l.split('\t')
            if temp[0] in ppid and temp[1] in ppid:
                p1 = ppid[temp[0]].replace("\n","")
                p2 = ppid[temp[1]].replace("\n","")
                fb.write(p1+'\t'+p2)
                fb.write("\n")
            l = fa.readline()
    fb.close()
# p_p()