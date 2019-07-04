#写对应的类别
def xieleibie():
    f = open('.\\data\\pup\\vector\\random_walks.txt','r', encoding='UTF-8', errors='ignore')
    line = f.readline()              		 # 调用文件的 readline()方法
    with open('.\\data\\pup\\vector\\node_type.txt', 'w') as fb:
        while line:
            list = line.strip().split(" ")
            for i in range(0,len(list)):
                if (i % 2 == 0):
                    fb.write(list[i]+" poi\n")
                    print(list[i]+" poi")
                elif(i % 2 == 1):
                    fb.write(list[i] + " user\n")
                    print(list[i]+" user")
            line = f.readline()
        f.close()

def quchong():
    a = 0
    readDir = ".\\data\\pup\\vector\\node_type.txt"  # old
    writeDir = ".\\data\\pup\\vector\\node_type_mapings.txt"  # new
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

#拆分类别逗号
def chaifen():
    f = open('C:\\Users\\HP\\Desktop\\poi_checkin.txt','r', encoding='UTF-8', errors='ignore')
    line = f.readline()              		 # 调用文件的 readline()方法
    with open('C:\\Users\\HP\\Desktop\\a.txt', 'a+') as fb:
        while line:
            list = line.strip().split("	")
            if list[2].__contains__(","):
                cate = list[2].split(",")
                for c in cate:
                    fb.write(list[0]+"\t"+list[1]+"\t"+c+"\n")
                    print(list[0]+"\t"+list[1]+"\t"+c)
            else:
                fb.write(list[0] + "\t" + list[1] + "\t" + list[2] + "\n")
                print(list[0] + "\t" + list[1] + "\t" + list[2])
            line = f.readline()
        f.close()

#time.loc
def dealTL():
    f = open('C:\\Users\\HP\\Desktop\\poi-time.txt','r', encoding='UTF-8', errors='ignore')
    line = f.readline()              		 # 调用文件的 readline()方法
    with open('C:\\Users\\HP\\Desktop\\a.txt', 'a+', encoding='UTF-8') as fb:
        fb.write("VenueId\tVenueCategory\n")
        while line:
            list = line.strip().split(",")
            # for l in list:
            #     print(l)
            # line = f.readline()
            if len(list) != 1:
                #userid
                fb.write(list[0]+"\t")
                print(list[0])
                #time
                if list[1].__contains__(" "):
                    time = list[1].split(" ")
                    for t in time:
                        if t.__contains__(":"):
                            detailtime = t.split(":")
                            for h in detailtime:
                                fb.write(h + "\t")
                                print(h)
                        else:
                            fb.write(t + "\t")
                            print(t)
                else:
                    fb.write(list[1] + "\t")
                    print(list[1])
                #poiid\location
                i = 2
                while(i < len(list)):
                    fb.write(list[i] + "\t")
                    print(list[i])
                    i = i+1
                fb.write("\n")
                line = f.readline()
            else:
                line = f.readline()
        f.close()

def dealcate():
    f = open('C:\\Users\\HP\\Desktop\\poi_category.txt','r', encoding='UTF-8', errors='ignore')
    line = f.readline()              		 # 调用文件的 readline()方法
    with open('C:\\Users\\HP\\Desktop\\poi_category_index.txt', 'a+', encoding='UTF-8') as fb:
        fb.write("VenueId\tVenueCategory\n")
        while line:
            list = line.strip().split(",")
            # for l in list:
            #     print(l)
            # line = f.readline()
            if len(list) >= 2:
                #category
                i = 1
                while(i < len(list)):
                    fb.write(list[0]+ "\t"+list[i] + "\n")
                    print(list[0]+ "\t"+list[i])
                    i = i+1
                line = f.readline()
            else:
                line = f.readline()
        f.close()

# dealcate()
xieleibie()
quchong()