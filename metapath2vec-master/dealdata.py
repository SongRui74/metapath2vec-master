#写对应的类别
def xieleibie(dirpath):
    f = open(dirpath + '\\random_walks.txt','r', encoding='UTF-8', errors='ignore')
    line = f.readline()              		 # 调用文件的 readline()方法
    with open(dirpath + '\\node_type.txt', 'w') as fb:
        while line:
            list = line.strip().split(" ")
            for i in range(0,len(list)):
                if (i % 2 == 0):
                    fb.write(list[i]+" user\n")
                    # print(list[i]+" user")
                elif(i % 2 == 1):
                    fb.write(list[i] + " poi\n")
                    # print(list[i]+" poi")
            line = f.readline()
        f.close()

def quchong(dirpath):
    a = 0
    readDir = dirpath + "\\node_type.txt"  # old
    writeDir = dirpath + "\\node_type_mapings.txt"  # new
    # txtDir = "/home/Administrator/Desktop/１"
    lines_seen = set()
    outfile = open(writeDir, "w")
    f = open(readDir, "r")
    for line in f:
        if line not in lines_seen:
            a += 1
            outfile.write(line)
            lines_seen.add(line)
            # print(a)
            # print('\n')
    outfile.close()
    print("success")

#写对应的类别
def xieleibie_upc(dirpath):
    f = open(dirpath + '\\random_walks.txt','r', encoding='UTF-8', errors='ignore')
    line = f.readline()              		 # 调用文件的 readline()方法
    with open(dirpath + '\\node_type.txt', 'w') as fb:
        while line:
            list = line.strip().split(" ")
            for i in range(0,len(list)):
                if (i % 4 == 0):
                    fb.write(list[i]+" user\n")
                    # print(list[i]+" user")
                elif(i % 4 == 1):
                    fb.write(list[i] + " poi\n")
                    # print(list[i]+" poi")
                elif (i % 4 == 2):
                    fb.write(list[i] + " category\n")
                    # print(list[i] + " category")
                elif (i % 4 == 3):
                    fb.write(list[i] + " poi\n")
                    # print(list[i] + " poi")
            line = f.readline()
        f.close()

#写对应的类别
def xieleibie_utlp(dirpath):
    f = open(dirpath + '\\random_walks.txt','r', encoding='UTF-8', errors='ignore')
    line = f.readline()              		 # 调用文件的 readline()方法
    with open(dirpath + '\\node_type.txt', 'w') as fb:
        while line:
            list = line.strip().split(" ")
            for i in range(0,len(list)):
                if (i % 4 == 0):
                    fb.write(list[i]+" user\n")
                    # print(list[i]+" user")
                elif(i % 4 == 1):
                    fb.write(list[i] + " tl\n")
                    # print(list[i]+" tl")
                elif (i % 4 == 2):
                    fb.write(list[i] + " poi\n")
                    # print(list[i] + " poi")
                elif (i % 4 == 3):
                    fb.write(list[i] + " tl\n")
                    # print(list[i] + " tl")
            line = f.readline()
        f.close()

# def xieleibie_utlpc(dirpath):
#     f = open(dirpath + '\\random_walks.txt','r', encoding='UTF-8', errors='ignore')
#     line = f.readline()              		 # 调用文件的 readline()方法
#     with open(dirpath + '\\node_type.txt', 'w') as fb:
#         while line:
#             list = line.strip().split(" ")
#             for i in range(0,len(list)):
#                 if (i % 6 == 0):
#                     fb.write(list[i]+" user\n")
#                     # print(list[i]+" user")
#                 elif(i % 6 == 1):
#                     fb.write(list[i] + " tl\n")
#                     # print(list[i]+" tl")
#                 elif (i % 6 == 2):
#                     fb.write(list[i] + " poi\n")
#                     # print(list[i] + " poi")
#                 elif (i % 6 == 3):
#                     fb.write(list[i] + " category\n")
#                     # print(list[i] + " category")
#                 elif (i % 6 == 4):
#                     fb.write(list[i] + " poi\n")
#                     # print(list[i] + " poi")
#                 elif (i % 6 == 5):
#                     fb.write(list[i] + " tl\n")
#                     # print(list[i] + " tl")
#             line = f.readline()
#         f.close()

################################################################################
#分割训练集80%和测试集20%
def train_testdata():
    delnum = 30#删除少于delnum 个签到的用户
    a = 0.8 #80%作为训练集
    data = '.\\data\\100user\\checkin.txt'
    train = '.\\data\\100user\\train.txt'
    test = '.\\data\\100user\\test.txt'

    #打开原文件
    f = open(data, 'r', encoding='UTF-8', errors='ignore')
    line = f.readline()

    fa = open(train, 'w')
    fb = open(test, 'w')
    fa.write(line)  #写列名
    fb.write(line)

    # 统计user_poi dict
    user_poilist = dict()
    while line:
        line = f.readline()
        toks = line.strip().split("\t")
        if len(toks) == 4: #17
            u, tl, p, c = toks[0], toks[1], toks[2], toks[3]
            # u, t, l, p, c = toks[0], toks[8], toks[9], toks[13], toks[16]
            # if u is not None and t is not None and l is not None and p is not None and c is not None:
            if u not in user_poilist:
                user_poilist[u] = []
            user_poilist[u].append(str(line))
    f.close()

    # #地点少于delnum的删除
    # for user in list(user_poilist):
    #     if len(user_poilist[user]) <= delnum:
    #         user_poilist.pop(user)

    #写入train&test，并且每一项不为空
    for user in user_poilist:
        num = int(a*len(user_poilist[user])) #训练集  每个用户的签到数量
        l = user_poilist[user]
        for i in range(0,num):
            fa.write(str(l[i]))

        for i in range(num,len(user_poilist[user])):
            fb.write(str(l[i]))

    fa.close()
    fb.close()

# train_testdata()

# upu = ".\\data\\upu\\vector"
# xieleibie(upu)
# quchong(upu)
#
# upcpu = ".\\data\\upcpu\\vector"
# xieleibie_upc(upcpu)
# quchong(upcpu)

# utlp= ".\\data\\utlp\\vector"
# xieleibie_utlp(utlp)
# quchong(utlp)


utlptlu= ".\\data\\utlptlu\\vector"
xieleibie_utlp(utlptlu)
quchong(utlptlu)

# utlpc= ".\\data\\utlpc\\vector"
# xieleibie_utlpc(utlpc)
# quchong(utlpc)



########################################################################################
# #拆分类别逗号
# def chaifen():
#     f = open('C:\\Users\\HP\\Desktop\\poi_checkin.txt','r', encoding='UTF-8', errors='ignore')
#     line = f.readline()              		 # 调用文件的 readline()方法
#     with open('C:\\Users\\HP\\Desktop\\a.txt', 'a+') as fb:
#         while line:
#             list = line.strip().split("	")
#             if list[2].__contains__(","):
#                 cate = list[2].split(",")
#                 for c in cate:
#                     fb.write(list[0]+"\t"+list[1]+"\t"+c+"\n")
#                     print(list[0]+"\t"+list[1]+"\t"+c)
#             else:
#                 fb.write(list[0] + "\t" + list[1] + "\t" + list[2] + "\n")
#                 print(list[0] + "\t" + list[1] + "\t" + list[2])
#             line = f.readline()
#         f.close()
#
# #time.loc
# def dealTL():
#     f = open('C:\\Users\\HP\\Desktop\\poi-time.txt','r', encoding='UTF-8', errors='ignore')
#     line = f.readline()              		 # 调用文件的 readline()方法
#     with open('C:\\Users\\HP\\Desktop\\a.txt', 'a+', encoding='UTF-8') as fb:
#         fb.write("VenueId\tVenueCategory\n")
#         while line:
#             list = line.strip().split(",")
#             # for l in list:
#             #     print(l)
#             # line = f.readline()
#             if len(list) != 1:
#                 #userid
#                 fb.write(list[0]+"\t")
#                 print(list[0])
#                 #time
#                 if list[1].__contains__(" "):
#                     time = list[1].split(" ")
#                     for t in time:
#                         if t.__contains__(":"):
#                             detailtime = t.split(":")
#                             for h in detailtime:
#                                 fb.write(h + "\t")
#                                 print(h)
#                         else:
#                             fb.write(t + "\t")
#                             print(t)
#                 else:
#                     fb.write(list[1] + "\t")
#                     print(list[1])
#                 #poiid\location
#                 i = 2
#                 while(i < len(list)):
#                     fb.write(list[i] + "\t")
#                     print(list[i])
#                     i = i+1
#                 fb.write("\n")
#                 line = f.readline()
#             else:
#                 line = f.readline()
#         f.close()
#
# def dealcate():
#     f = open('C:\\Users\\HP\\Desktop\\poi_category.txt','r', encoding='UTF-8', errors='ignore')
#     line = f.readline()              		 # 调用文件的 readline()方法
#     with open('C:\\Users\\HP\\Desktop\\poi_category_index.txt', 'a+', encoding='UTF-8') as fb:
#         fb.write("VenueId\tVenueCategory\n")
#         while line:
#             list = line.strip().split(",")
#             # for l in list:
#             #     print(l)
#             # line = f.readline()
#             if len(list) >= 2:
#                 #category
#                 i = 1
#                 while(i < len(list)):
#                     fb.write(list[0]+ "\t"+list[i] + "\n")
#                     print(list[0]+ "\t"+list[i])
#                     i = i+1
#                 line = f.readline()
#             else:
#                 line = f.readline()
#         f.close()

