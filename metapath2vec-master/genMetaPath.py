import sys
import os
import random
from collections import Counter


class MetaPathGenerator:
    def __init__(self):
        self.id_user = dict()
        self.id_poi = dict()
        self.id_cate = dict()
        self.id_tl = dict()
        self.poi_userlist = dict()
        self.user_poilist = dict()
        self.poi_catelist = dict()
        self.cate_poilist = dict()
        self.user_tllist = dict()
        self.tl_userlist = dict()
        self.poi_tllist = dict()
        self.tl_poilist = dict()

        self.poi_poilist = dict()

        # self.id_author = dict()
        # self.id_conf = dict()
        # self.author_coauthorlist = dict()
        # self.conf_authorlist = dict()
        # self.author_conflist = dict()
        # self.paper_author = dict()
        # self.author_paper = dict()
        # self.conf_paper = dict()
        # self.paper_conf = dict()
    def readtestdata(self, dirpath):
        self.id_poi.clear()
        self.id_user.clear()
        self.poi_userlist.clear()
        self.user_poilist.clear()

        with open(dirpath + "\\id_user.txt",'r', encoding='ISO-8859-1') as adictfile:
            for line in adictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    self.id_user[toks[0]] = toks[1].replace(" ", "")
        #Python replace() 方法把字符串中的 old（旧字符串） 替换成 new(新字符串)，如果指定第三个参数max，则替换不超过 max 次。
        #id_author={dict}{'89376': 'aRuiJiang', '36606': 'aDanConescu'.....}
        #print "#authors", len(self.id_author)

        with open(dirpath + "\\id_poi.txt",'r', encoding='ISO-8859-1') as cdictfile:
            for line in cdictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    self.id_poi[toks[0]] = toks[0]

        with open(dirpath + "\\user_poi.txt",'r', encoding='ISO-8859-1') as pafile:
            for line in pafile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    u, p = toks[0], toks[1]
                    #u:'37',p:'4e3e097552b1a04aff2139ff'
                    if u not in self.user_poilist:
                        self.user_poilist[u] = []
                    self.user_poilist[u].append(p)
                    if p not in self.poi_userlist:
                        self.poi_userlist[p] = []
                    self.poi_userlist[p].append(u)
                #poi_user:{'21525':['33467','33467','33468'}]}
                #user_poi:{'33467':['21525'],'33468':['21525']}

    #构造
    #conf=poi,author=user 重写readdata和generate
    def read_upudata(self, dirpath):
        self.id_poi.clear()
        self.id_user.clear()
        self.poi_userlist.clear()
        self.user_poilist.clear()

        with open(dirpath + "\\id_user.txt",'r', encoding='ISO-8859-1') as adictfile:
            for line in adictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    self.id_user[toks[0]] = toks[1].replace(" ", "")
        #Python replace() 方法把字符串中的 old（旧字符串） 替换成 new(新字符串)，如果指定第三个参数max，则替换不超过 max 次。
        #id_author={dict}{'89376': 'aRuiJiang', '36606': 'aDanConescu'.....}
        #print "#authors", len(self.id_author)

        with open(dirpath + "\\id_poi.txt",'r', encoding='ISO-8859-1') as cdictfile:
            for line in cdictfile:
                toks = line.strip().split("\t")
                if len(toks) == 3:
                    self.id_poi[toks[0]] = toks[0]

        with open(dirpath + "\\user_poi.txt",'r', encoding='ISO-8859-1') as pafile:
            for line in pafile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    u, p = toks[0], toks[1]
                    #u:'37',p:'4e3e097552b1a04aff2139ff'
                    if u not in self.user_poilist:
                        self.user_poilist[u] = []
                    self.user_poilist[u].append(p)
                    if p not in self.poi_userlist:
                        self.poi_userlist[p] = []
                    self.poi_userlist[p].append(u)
                #poi_user:{'21525':['33467','33467','33468'}]}
                #user_poi:{'33467':['21525'],'33468':['21525']}
    def generate_random_upu(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding="ISO-8859-1")
        for user in self.user_poilist:
            user0 = user
            for j in range(0, numwalks):  # wnum walks以每个起点行走的路径的数量。以poi0为起点，随机numwalks个路径。
                outline = self.id_user[user0]  # outline='vADB'即122会议的名称
                for i in range(0, walklength):  # 行走的长度走一次是一个VAV，走walklength次，长度为2*walklength+1
                    pois = self.user_poilist[user]
                    numa = len(pois)  # numa代表用户u对应的地点个数
                    poiid = random.randrange(numa)
                    poi = pois[poiid]
                    outline += " " + self.id_poi[poi]  # 路径UP

                    users = self.poi_userlist[poi]
                    numa = len(users)  # numa代表该会议122的作者人数38
                    userid = random.randrange(numa)  # 将作者顺序打乱authorid=随机数28每次都不一样，但是为38中的一个数字
                    # authorid = 28
                    # randrange() 方法返回指定递增基数集合中的一个随机数，基数缺省值为1。
                    user = users[userid]  # 随机authorid的作者编号='33491' #将打乱的作者重新放入author
                    outline += " " + self.id_user[user]  # 将会议名称和作者名称以空格连接{'vADB' 'aJ.Maguire'}
                outfile.write(outline + "\n")  # 产生多个PUPUP的序列。
        outfile.close()

    def read_upcdata(self, dirpath):
        self.id_poi.clear()
        self.id_user.clear()
        self.id_cate.clear()
        self.poi_userlist.clear()
        self.user_poilist.clear()
        self.poi_catelist.clear()
        self.cate_poilist.clear()

        with open(dirpath + "\\id_user.txt",'r', encoding='ISO-8859-1') as adictfile:
            for line in adictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    self.id_user[toks[0]] = toks[1].replace(" ", "")

        with open(dirpath + "\\id_poi.txt",'r', encoding='ISO-8859-1') as cdictfile:
            for line in cdictfile:
                toks = line.strip().split("\t")
                if len(toks) == 3:
                    self.id_poi[toks[0]] = toks[0]

        with open(dirpath + "\\id_category.txt",'r', encoding='ISO-8859-1') as cdictfile:
            for line in cdictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    newpoi = toks[1].replace(" ", "")
                    self.id_cate[toks[0]] = toks[0]

        with open(dirpath + "\\user_poi_cate.txt",'r', encoding='ISO-8859-1') as pafile:
            for line in pafile:
                toks = line.strip().split("\t")
                if len(toks) == 3:
                    u, p, c = toks[0], toks[1], toks[2]
                    #u:'37',p:'4e3e097552b1a04aff2139ff'
                    if u not in self.user_poilist:
                        self.user_poilist[u] = []
                    self.user_poilist[u].append(p)
                    if p not in self.poi_userlist:
                        self.poi_userlist[p] = []
                    self.poi_userlist[p].append(u)
                    # poi_user:{'21525':['33467','33467','33468'}]}
                    # user_poi:{'33467':['21525'],'33468':['21525']}
                    if p not in self.poi_catelist:
                        self.poi_catelist[p] = c
                    if c not in self.cate_poilist:
                        self.cate_poilist[c] = []
                    self.cate_poilist[c].append(p)
    def generate_random_upcpu(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding="ISO-8859-1")
        for user in self.user_poilist:
            user0 = user
            for j in range(0, numwalks):
                outline = self.id_user[user0]  #路径U
                for i in range(0, walklength):
                    pois = self.user_poilist[user]
                    numa = len(pois)  # numa代表用户u对应的地点个数
                    poiid = random.randrange(numa)
                    poi = pois[poiid]
                    outline += " " + self.id_poi[poi]  #路径UP

                    cate = self.poi_catelist[poi]
                    outline += " " + cate   #路径UPC  #id 更改为 c+类别id  区别于其他实体的数字id

                    pois = self.cate_poilist[cate]  #类别对应的地点
                    numc = len(pois)   #numc代表类别c对应的poi个数
                    poiid = random.randrange(numc)
                    poi = pois[poiid]
                    outline += " " + self.id_poi[poi]    #路径UPCP
                    users = self.poi_userlist[poi]  # 地点对应的用户
                    numu = len(users)
                    userid = random.randrange(numu)
                    user = users[userid]
                    outline += " " + self.id_user[user]  #路径UPCPU
                outfile.write(outline + "\n")
        outfile.close()

    def read_utlpdata(self, dirpath):
        self.id_poi.clear()
        self.id_user.clear()
        self.id_tl.clear()
        self.user_tllist.clear()
        self.tl_userlist.clear()
        self.tl_poilist.clear()
        self.poi_tllist.clear()

        with open(dirpath + "\\id_user.txt",'r', encoding='ISO-8859-1') as adictfile:
            for line in adictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    self.id_user[toks[0]] = toks[1].replace(" ", "")

        with open(dirpath + "\\id_poi.txt",'r', encoding='ISO-8859-1') as cdictfile:
            for line in cdictfile:
                toks = line.strip().split("\t")
                if len(toks) == 3:
                    self.id_poi[toks[0]] = toks[0]

        with open(dirpath + "\\id_tl.txt",'r', encoding='ISO-8859-1') as cdictfile:
            for line in cdictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    self.id_tl[toks[0]] = toks[1]  #tl的id，tl内容
        with open(dirpath + "\\user_tl_poi.txt",'r', encoding='ISO-8859-1') as pafile:
            for line in pafile:
                toks = line.strip().split("\t")
                if len(toks) == 3:
                    u, tl, p = toks[0], toks[1], toks[2]  #tokes[2]是类别名称，toks[3]是类别id
                    #u:'37',p:'4e3e097552b1a04aff2139ff'
                    if u not in self.user_tllist:
                        self.user_tllist[u] = []
                    self.user_tllist[u].append(tl)
                    if tl not in self.tl_userlist:
                        self.tl_userlist[tl] = []
                    self.tl_userlist[tl].append(u)
                    # poi_user:{'21525':['33467','33467','33468'}]}
                    # user_poi:{'33467':['21525'],'33468':['21525']}
                    if p not in self.poi_tllist:
                        self.poi_tllist[p] = []
                    self.poi_tllist[p].append(tl)
                    if tl not in self.tl_poilist:
                        self.tl_poilist[tl] = []
                    self.tl_poilist[tl].append(p)
    def generate_random_utlptlu(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding="ISO-8859-1")
        for user in self.user_tllist:
            user0 = user
            #随机初始tl0
            tls = self.user_tllist[user]
            tlid0 = random.randrange(len(tls))
            tl0 = tls[tlid0]
            h0 = self.id_tl[tl0][0:2]
            l0 = self.id_tl[tl0][2:]

            for j in range(0, numwalks):
                outline = self.id_user[user0]  #路径U
                for i in range(0, walklength):
                    tls = self.user_tllist[user]
                    numtl = len(tls)
                    while(1):
                        tlid = random.randrange(numtl)
                        tl = tls[tlid]
                        h = self.id_tl[tl][0:2]
                        l = self.id_tl[tl][2:]
                        if abs(int(h)-int(h0)) < 4 and str(l).__eq__(l0):  #时间邻域，上下3个小时
                            outline += " " + tl  #路径U TL
                            h0 = h
                            l0 = l
                            break

                    pois = self.tl_poilist[tl]  #时空对应的地点
                    nump = len(pois)
                    poiid = random.randrange(nump)
                    poi = pois[poiid]
                    outline += " " + self.id_poi[poi]    #路径U TL P

                    tls = self.poi_tllist[poi]
                    numtl = len(tls)
                    while (1):
                        tlid = random.randrange(numtl)
                        tl = tls[tlid]
                        h = self.id_tl[tl][0:2]
                        l = self.id_tl[tl][2:]
                        if abs(int(h) - int(h0)) < 4 and str(l).__eq__(l0):  #时间邻域，上下3个小时
                            outline += " " + tl  # 路径U TL P TL
                            h0 = h
                            l0 = l
                            break
                    # tlid = random.randrange(numtl)
                    # tl = tls[tlid]
                    # outline += " " + self.id_tl[tl]

                    users = self.tl_userlist[tl] # 地点对应的用户
                    numu = len(users)
                    userid = random.randrange(numu)
                    user = users[userid]
                    outline += " " + self.id_user[user]  #路径U TL P TL U
                outfile.write(outline + "\n")
        outfile.close()

    def generate_random_utp(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding="ISO-8859-1")
        for user in self.user_tllist:
            user0 = user
            #随机初始tl0
            tls = self.user_tllist[user]
            tlid0 = random.randrange(len(tls))
            tl0 = tls[tlid0]
            h0 = self.id_tl[tl0][0:2]

            for j in range(0, numwalks):
                outline = self.id_user[user0]  #路径U
                for i in range(0, walklength):
                    tls = self.user_tllist[user]
                    numtl = len(tls)
                    while(1):
                        tlid = random.randrange(numtl)
                        tl = tls[tlid]
                        h = self.id_tl[tl][0:2]
                        if abs(int(h)-int(h0)) < 4:  #时间邻域，上下3个小时
                            outline += " " + tl  #路径U TL
                            h0 = h
                            break

                    pois = self.tl_poilist[tl]  #时空对应的地点
                    nump = len(pois)
                    poiid = random.randrange(nump)
                    poi = pois[poiid]
                    outline += " " + self.id_poi[poi]    #路径U T P

                    tls = self.poi_tllist[poi]
                    numtl = len(tls)
                    while (1):
                        tlid = random.randrange(numtl)
                        tl = tls[tlid]
                        h = self.id_tl[tl][0:2]
                        if abs(int(h) - int(h0)) < 4:  #时间邻域，上下3个小时
                            outline += " " + tl  # 路径U T P T
                            h0 = h
                            break
                    # tlid = random.randrange(numtl)
                    # tl = tls[tlid]
                    # outline += " " + self.id_tl[tl]

                    users = self.tl_userlist[tl] # 地点对应的用户
                    numu = len(users)
                    userid = random.randrange(numu)
                    user = users[userid]
                    outline += " " + self.id_user[user]  #路径U T P T U
                outfile.write(outline + "\n")
        outfile.close()

    def generate_random_ulp(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding="ISO-8859-1")
        for user in self.user_tllist:
            user0 = user
            #随机初始tl0
            tls = self.user_tllist[user]
            tlid0 = random.randrange(len(tls))
            tl0 = tls[tlid0]
            l0 = self.id_tl[tl0][2:]

            for j in range(0, numwalks):
                outline = self.id_user[user0]  #路径U
                for i in range(0, walklength):
                    tls = self.user_tllist[user]
                    numtl = len(tls)
                    while(1):
                        tlid = random.randrange(numtl)
                        tl = tls[tlid]
                        l = self.id_tl[tl][2:]
                        if str(l).__eq__(l0):  #时间邻域，上下3个小时
                            outline += " " + tl  #路径U TL
                            l0 = l
                            break

                    pois = self.tl_poilist[tl]  #时空对应的地点
                    nump = len(pois)
                    poiid = random.randrange(nump)
                    poi = pois[poiid]
                    outline += " " + self.id_poi[poi]    #路径U L P

                    tls = self.poi_tllist[poi]
                    numtl = len(tls)
                    while (1):
                        tlid = random.randrange(numtl)
                        tl = tls[tlid]
                        l = self.id_tl[tl][2:]
                        if str(l).__eq__(l0):  #时间邻域，上下3个小时
                            outline += " " + tl  # 路径U L P L
                            l0 = l
                            break
                    users = self.tl_userlist[tl] # 地点对应的用户
                    numu = len(users)
                    userid = random.randrange(numu)
                    user = users[userid]
                    outline += " " + self.id_user[user]  #路径U L P L U
                outfile.write(outline + "\n")
        outfile.close()

    def read_uppudata(self, dirpath):
        self.id_poi.clear()
        self.id_user.clear()
        self.poi_userlist.clear()
        self.user_poilist.clear()
        self.poi_poilist.clear()

        with open(dirpath + "\\id_user.txt",'r', encoding='ISO-8859-1') as adictfile:
            for line in adictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    self.id_user[toks[0]] = toks[1].replace(" ", "")
        #Python replace() 方法把字符串中的 old（旧字符串） 替换成 new(新字符串)，如果指定第三个参数max，则替换不超过 max 次。
        #id_author={dict}{'89376': 'aRuiJiang', '36606': 'aDanConescu'.....}
        #print "#authors", len(self.id_author)

        with open(dirpath + "\\id_poi.txt",'r', encoding='ISO-8859-1') as cdictfile:
            for line in cdictfile:
                toks = line.strip().split("\t")
                if len(toks) == 3:
                    self.id_poi[toks[0]] = toks[0]

        with open(dirpath + "\\user_poi.txt",'r', encoding='ISO-8859-1') as pafile:
            for line in pafile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    u, p = toks[0], toks[1]
                    #u:'37',p:'4e3e097552b1a04aff2139ff'
                    if u not in self.user_poilist:
                        self.user_poilist[u] = []
                    self.user_poilist[u].append(p)
                    if p not in self.poi_userlist:
                        self.poi_userlist[p] = []
                    self.poi_userlist[p].append(u)
                #poi_user:{'21525':['33467','33467','33468'}]}
                #user_poi:{'33467':['21525'],'33468':['21525']}

        with open(dirpath + "\\poi_poi.txt",'r', encoding='ISO-8859-1') as pafile:
            for line in pafile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    p1, p2 = toks[0], toks[1]
                    if p1 not in self.poi_poilist:
                        self.poi_poilist[p1] = []
                    self.poi_poilist[p1].append(p2)
                    if p2 not in self.poi_poilist:
                        self.poi_poilist[p2] = []
                    self.poi_poilist[p2].append(p1)
    def generate_random_uppu(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding="ISO-8859-1")
        for user in self.user_poilist:
            user0 = user
            for j in range(0, numwalks):
                outline = self.id_user[user0]  # 路径U
                for i in range(0, walklength):
                    poi1s = self.user_poilist[user]
                    numa = len(poi1s)
                    poiid = random.randrange(numa)
                    poi1 = poi1s[poiid]
                    outline += " " + self.id_poi[poi1]  # 路径UP

                    if poi1 not in self.poi_poilist:
                        continue

                    poi2s = self.poi_poilist[poi1]
                    numb = len(poi2s)
                    poiid = random.randrange(numb)
                    poi2 = poi2s[poiid]
                    outline += " " + self.id_poi[poi2]  # 路径UPP

                    if poi2 not in self.poi_userlist:
                        continue

                    users = self.poi_userlist[poi2]
                    numa = len(users)
                    userid = random.randrange(numa)
                    user = users[userid]
                    outline += " " + self.id_user[user]  # 路径UPPU
                outfile.write(outline + "\n")
        outfile.close()

dirpath = ".\\data\\upu\\input"
upuoutfilename = ".\\data\\upu\\vector\\random_walks.txt"

# dirpath = ".\\data\\test\\input"
# upuoutfilename = ".\\data\\test\\vector\\random_walks.txt"

upc_dirpath = ".\\data\\upcpu\\input"
upc_outfilename = ".\\data\\upcpu\\vector\\random_walks.txt"

utp_dirpath = ".\\data\\utp\\input"
utp_outfilename = ".\\data\\utp\\vector\\random_walks.txt"

ulp_dirpath = ".\\data\\ulp\\input"
ulp_outfilename = ".\\data\\ulp\\vector\\random_walks.txt"

utlptlu_dirpath = ".\\data\\utlptlu\\input"
utlptlu_outfilename = ".\\data\\utlptlu\\vector\\random_walks.txt"

uppu_dirpath = ".\\data\\uppu\\input"
uppu_outfilename = ".\\data\\uppu\\vector\\random_walks.txt"

if __name__ == "__main__":
    numwalks = 20  #同一个起点开始的路径的数量
    walklength = 10  #路径长度
    mpg = MetaPathGenerator()

    # mpg.read_upudata(dirpath)
    # mpg.generate_random_upu(upuoutfilename, numwalks, walklength)

    # mpg.read_upcdata(upc_dirpath)
    # mpg.generate_random_upcpu(upc_outfilename,numwalks, walklength)

    # mpg.read_utlpdata(utp_dirpath)
    # mpg.generate_random_utp(utp_outfilename, numwalks, walklength)
    #
    # mpg.read_utlpdata(ulp_dirpath)
    # mpg.generate_random_ulp(ulp_outfilename, numwalks, walklength)

    # mpg.read_utlpdata(utlptlu_dirpath)
    # mpg.generate_random_utlptlu(utlptlu_outfilename, numwalks, walklength)

    mpg.read_uppudata(uppu_dirpath)
    mpg.generate_random_uppu(uppu_outfilename, numwalks, walklength)


###########################################################################################################################
#     def read_data(self, dirpath):
#         with open(dirpath + "\\id_author.txt",'r', encoding='ISO-8859-1') as adictfile:
#             for line in adictfile:
#                 toks = line.strip().split("\t")
#                 if len(toks) == 2:
#                     self.id_author[toks[0]] = toks[1].replace(" ", "")
#         #Python replace() 方法把字符串中的 old（旧字符串） 替换成 new(新字符串)，如果指定第三个参数max，则替换不超过 max 次。
#         #id_author={dict}{'89376': 'aRuiJiang', '36606': 'aDanConescu'.....}
#         #print "#authors", len(self.id_author)
#
#         with open(dirpath + "\\id_conf.txt",'r', encoding='ISO-8859-1') as cdictfile:
#             for line in cdictfile:
#                 toks = line.strip().split("\t")
#                 if len(toks) == 2:
#                     newconf = toks[1].replace(" ", "")
#                     self.id_conf[toks[0]] = newconf
#
#         #print "#conf", len(self.id_conf)
#
#         with open(dirpath + "\\paper_author.txt",'r', encoding='ISO-8859-1') as pafile:
#             for line in pafile:
#                 toks = line.strip().split("\t")
#                 if len(toks) == 2:
#                     p, a = toks[0], toks[1]
#                     #p:'21525',a:'33467'
#                     if p not in self.paper_author:
#                         self.paper_author[p] = []
#                     self.paper_author[p].append(a)
#                     if a not in self.author_paper:
#                         self.author_paper[a] = []
#                     self.author_paper[a].append(p)
#                 #paper_author:{'21525':['33467','33467','33468'}]}
#                 #author_paper:{'33467':['21525'],'33468':['21525']}
#         with open(dirpath + "\\paper_conf.txt",'r', encoding='ISO-8859-1') as pcfile:
#             for line in pcfile:
#                 toks = line.strip().split("\t")
#                 if len(toks) == 2:
#                     p, c = toks[0], toks[1]
#                     self.paper_conf[p] = c
#                     if c not in self.conf_paper:
#                         self.conf_paper[c] = []
#                     self.conf_paper[c].append(p)
#         #paper_conf:{'21525':'122','21526':'122'}
#         #conf_paper:{'122':['21525','21526']}
#         sumpapersconf, sumauthorsconf = 0, 0
#         #sumpapersconf=33, sumauthorsconf = 2
#         conf_authors = dict()
#         for conf in self.conf_paper: #conf指的是conf_paper的index。conf='122'
#             papers = self.conf_paper[conf] #paper=conf_paper[conf]指的是index对应的value。['21525','21526','21527'....]
#             sumpapersconf += len(papers) #sumpapersconf为某一会议对应的文章的数量。
#             for paper in papers: #'21525'
#                 if paper in self.paper_author:
#                     authors = self.paper_author[paper] #在paper_author中查找会议122的文章’21525‘，对应的作者。
#                     sumauthorsconf += len(authors) #将所有作者数量保存在sumauthorsconf
#         #authors中记录了所有的作者。
#
#         print ("#confs  ", len(self.conf_paper))
#         print ("#papers ", sumpapersconf,  "#papers per conf ", sumpapersconf / len(self.conf_paper))
#         print ("#authors", sumauthorsconf, "#authors per conf", sumauthorsconf / len(self.conf_paper))
# #confs   2(会议的个数)
# #papers  164 #papers per conf 82.0(每个会议中的文章数量)
# #authors 38 #authors per conf 19.0(每个会议中包含的作者)
#
#     def generate_random_aca(self, outfilename, numwalks, walklength):
#         for conf in self.conf_paper:
#             self.conf_authorlist[conf] = [] #指的是{'122':[]}
#             for paper in self.conf_paper[conf]:
#                 if paper not in self.paper_author: continue
#                 for author in self.paper_author[paper]:
#                     self.conf_authorlist[conf].append(author)  #构建会议-作者列表conf_authorlist
#                     if author not in self.author_conflist:
#                         self.author_conflist[author] = []
#                     self.author_conflist[author].append(conf)
#         #print "author-conf list done"
#
#         outfile = open(outfilename, 'w', encoding="ISO-8859-1")
#         for conf in self.conf_authorlist:
#             conf0 = conf
#             for j in range(0, numwalks): #wnum walks每个节点的行走数。以会议为起点，每个会议要走100个VAV；走1000遍=会议个数464*1000遍=464000条
#                 outline = self.id_conf[conf0]#outline='vADB'即122会议的名称
#                 for i in range(0, walklength):#行走的长度走一次是一个VAV，走100次
#                     authors = self.conf_authorlist[conf]
#                     numa = len(authors)#numa代表该会议122的作者人数38
#                     authorid = random.randrange(numa)#将作者顺序打乱authorid=随机数28每次都不一样，但是为38中的一个数字
#                     #authorid = 28
#                     #randrange() 方法返回指定递增基数集合中的一个随机数，基数缺省值为1。
#                     author = authors[authorid] #随机authorid的作者编号='33491' #将打乱的作者重新放入author
#                     outline += " " + self.id_author[author]#将会议名称和作者名称以空格连接{'vADB' 'aJ.Maguire'}
#                     confs = self.author_conflist[author]#作者对应的会议
#                     numc = len(confs)
#                     confid = random.randrange(numc)
#                     conf = confs[confid]
#                     outline += " " + self.id_conf[conf]#outline={'vADB aJ.Maguire vADB'}
#                 outfile.write(outline + "\n")# 产生AVAVAVA的序列。产生多个AVAVA的序列。
#         outfile.close()
# '''
# 最后的结果类似：vADB aArieSegev vADB aAlejandroP.Buchmann vADB aHeinrichJasper vADB
# vSWDB aIoanaManolescu vWWW aDionysiosKostoulas vWWW aWernerRetschitzegger vKyotoInternationalConferenceonDigitalLibraries aHorstEidenberger vDELOSConference aCostantinoGrana vDELOSConference aNicolaFerro vIRCDL aTizianaCatarci vADL aSteceyE.Polonkey vADL aNaphtaliRishe vCIKM aXueLi vAPWeb aHaiZhuge vAPWeb aQingPingTan vAPWeb aKeunHoRyu vDASFAA aKuniakiUehara vDASFAA aRonSacks-Davis vSIGMODRecord aShashiK.Gadia vVLDB aSudarshanS.Chawathe vVLDB
# 形式为VAVAVA.
# '''
#python py4genMetaPaths.py 1000 100 net_aminer output.aminer.w1000.l100.txt
#python py4genMetaPaths.py 1000 100 net_dbis   output.dbis.w1000.l100.txt

#dirpath = "net_aminer"
# OR
#dirpath = "net_dbis"

# dirpath = ".\\data\\pup\\metapath"
# newoutfilename = ".\\data\\pup\\vector\\random_walks.txt"
# # outfilename = "E:\\#study\\Experiment\\(metapath2vec)\\data\\net_dbis\\output.txt"
#
# if __name__ == "__main__":
#     numwalks = 50  #同一个起点开始的路径的数量
#     walklength = 20  #路径长度
#     mpg = MetaPathGenerator()
#     mpg.read_newdata(dirpath)
#     mpg.generate_random_upu(newoutfilename, numwalks, walklength)
#     # mpg.read_data(dirpath)
#     # mpg.generate_random_aca(outfilename, numwalks, walklength)

