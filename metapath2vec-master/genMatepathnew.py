import sys
import os
import random
from collections import Counter


class MetaPathGenerator:
    def __init__(self):
        self.user = []
        self.poi = []
        self.id_tl = dict()  # tlid  tlcontent

        self.utl_p = dict()
        self.u_tl = dict()
        self.p_tl = dict()
        self.ptl_u = dict()

    def readtrain(self,dirpath):
        tl_id = dict()
        with open(dirpath + "\\id_tl.txt",'r', encoding='ISO-8859-1') as adictfile:
            for line in adictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    tl_id[toks[0]] = toks[1]  #"tlxx  string"

        with open(dirpath + "\\relation2id.txt",'r', encoding='ISO-8859-1') as adictfile:
            for line in adictfile:
                toks = line.strip().split("\t")   #"tlxx  0"
                if len(toks) == 2:
                    self.id_tl[toks[1]] = tl_id[toks[0]] # get "0  string"

        with open(dirpath + "\\train2id.txt",'r', encoding='ISO-8859-1') as adictfile:
            for line in adictfile:
                toks = line.strip().split("\t")
                if len(toks) == 3:
                    u,p,tl = toks[0],toks[1],toks[2]
                    self.user.append(u)
                    self.poi.append(p)

                    if (u,tl) not in self.utl_p:
                        self.utl_p[(u,tl)] = []
                    self.utl_p[(u,tl)].append(p)

                    if u not in self.u_tl:
                        self.u_tl[u] = []
                    self.u_tl[u].append(tl)

                    if p not in self.p_tl:
                        self.p_tl[p] = []
                    self.p_tl[p].append(tl)

                    if (p,tl) not in self.ptl_u:
                        self.ptl_u[(p,tl)] = []
                    self.ptl_u[(p,tl)].append(u)

        self.user = set(self.user)
        self.poi = set(self.poi)

    def generate_random(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding="ISO-8859-1")
        for user in self.user:
            user0 = user
            #随机初始tl
            tls = self.u_tl[user0]
            tlid = random.randrange(len(tls))
            tl0 = tls[tlid]
            # 获取具体时间和位置信息
            t0 = self.id_tl[tl0][0:2]
            l0 = self.id_tl[tl0][2:]

            for j in range(0, numwalks):
                outline = "u"+user0  # 路径U
                for i in range(0, walklength):
                    #tl节点
                    tls = self.u_tl[user]
                    while (1):
                        tlid = random.randrange(len(tls))
                        tl = tls[tlid]
                        t = self.id_tl[tl][0:2]
                        l = self.id_tl[tl][2:]
                        if abs(int(t)-int(t0)) < 4 and str(l).__eq__(l0):  #时间邻域，上下3个小时
                            outline += " tl" + tl  #路径U TL
                            break

                    #p节点
                    pois = self.utl_p[(user,tl)]
                    poiid = random.randrange(len(pois))
                    poi = pois[poiid]
                    outline += " p" + str(poi)  # 路径U TL P

                    # tl节点
                    tls = self.p_tl[poi]
                    while (1):
                        tlid = random.randrange(len(tls))
                        tl = tls[tlid]
                        t = self.id_tl[tl][0:2]
                        l = self.id_tl[tl][2:]
                        if abs(int(t) - int(t0)) < 4 and str(l).__eq__(l0):  # 时间邻域，上下3个小时
                            outline += " tl" + tl  # 路径U TL
                            break

                    # u节点
                    users = self.ptl_u[(poi, tl)]
                    userid = random.randrange(len(users))
                    user = users[userid]
                    outline += " u" + user  # 路径U TL P TL U
                outfile.write(outline + "\n")
        outfile.close()


dirpath = ".\\data\\Foursquare"
outfilename = ".\\data\\Foursquare\\output\\random_walks.txt"

if __name__ == "__main__":
    numwalks = 20  #同一个起点开始的路径的数量
    walklength = 10  #路径长度
    mpg = MetaPathGenerator()

    mpg.readtrain(dirpath)
    mpg.generate_random(outfilename, numwalks, walklength)
