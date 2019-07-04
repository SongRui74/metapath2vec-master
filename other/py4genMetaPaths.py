import sys
import os
import random
from collections import Counter


class MetaPathGenerator:
	def __init__(self):
		self.id_author = dict()
		self.id_conf = dict()
		self.author_coauthorlist = dict()
		self.conf_authorlist = dict()
		self.author_conflist = dict()
		self.paper_author = dict()
		self.author_paper = dict()
		self.conf_paper = dict()
		self.paper_conf = dict()

	def read_data(self, dirpath):
		with open(dirpath + "\\id_author.txt",'r', encoding='ISO-8859-1') as adictfile:
			for line in adictfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					self.id_author[toks[0]] = toks[1].replace(" ", "")
		#Python replace() 方法把字符串中的 old（旧字符串） 替换成 new(新字符串)，如果指定第三个参数max，则替换不超过 max 次。
		#id_author={dict}{'89376': 'aRuiJiang', '36606': 'aDanConescu'.....}
		#print "#authors", len(self.id_author)

		with open(dirpath + "\\id_conf.txt",'r', encoding='ISO-8859-1') as cdictfile:
			for line in cdictfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					newconf = toks[1].replace(" ", "")
					self.id_conf[toks[0]] = newconf

		#print "#conf", len(self.id_conf)

		with open(dirpath + "\\paper_author.txt",'r', encoding='ISO-8859-1') as pafile:
			for line in pafile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					p, a = toks[0], toks[1]
					#p:'21525',a:'33467'
					if p not in self.paper_author:
						self.paper_author[p] = []
					self.paper_author[p].append(a)
					if a not in self.author_paper:
						self.author_paper[a] = []
					self.author_paper[a].append(p)
				#paper_author:{'21525':['33467','33467','33468'}]}
				#author_paper:{'33467':['21525'],'33468':['21525']}
		with open(dirpath + "\\paper_conf.txt",'r', encoding='ISO-8859-1') as pcfile:
			for line in pcfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					p, c = toks[0], toks[1]
					self.paper_conf[p] = c 
					if c not in self.conf_paper:
						self.conf_paper[c] = []
					self.conf_paper[c].append(p)
		#paper_conf:{'21525':'122','21526':'122'}
		#conf_paper:{'122':['21525','21526']}
		sumpapersconf, sumauthorsconf = 0, 0
		#sumpapersconf=33, sumauthorsconf = 2
		conf_authors = dict()
		for conf in self.conf_paper: #conf指的是conf_paper的index。conf='122'
			papers = self.conf_paper[conf] #paper=conf_paper[conf]指的是index对应的value。['21525','21526','21527'....]
			sumpapersconf += len(papers) #sumpapersconf为某一会议对应的文章的数量。
			for paper in papers: #'21525'
				if paper in self.paper_author:
					authors = self.paper_author[paper] #在paper_author中查找会议122的文章’21525‘，对应的作者。
					sumauthorsconf += len(authors) #将所有作者数量保存在sumauthorsconf
		#authors中记录了所有的作者。

		print ("#confs  ", len(self.conf_paper))
		print ("#papers ", sumpapersconf,  "#papers per conf ", sumpapersconf / len(self.conf_paper))
		print ("#authors", sumauthorsconf, "#authors per conf", sumauthorsconf / len(self.conf_paper))
#confs   2(会议的个数)
#papers  164 #papers per conf 82.0(每个会议中的文章数量)
#authors 38 #authors per conf 19.0(每个会议中包含的作者)

	def generate_random_aca(self, outfilename, numwalks, walklength):
		for conf in self.conf_paper:
			self.conf_authorlist[conf] = [] #指的是{'122':[]}
			for paper in self.conf_paper[conf]:
				if paper not in self.paper_author: continue
				for author in self.paper_author[paper]:
					self.conf_authorlist[conf].append(author)  #构建会议-作者列表conf_authorlist
					if author not in self.author_conflist:
						self.author_conflist[author] = []
					self.author_conflist[author].append(conf)
		#print "author-conf list done"

		outfile = open(outfilename, 'w', encoding="ISO-8859-1")
		for conf in self.conf_authorlist:
			conf0 = conf
			for j in range(0, numwalks ): #wnum walks每个节点的行走数。以会议为起点，每个会议要走100个VAV；走1000遍=会议个数464*1000遍=464000条
				outline = self.id_conf[conf0]#outline='vADB'即122会议的名称
				for i in range(0, walklength):#行走的长度走一次是一个VAV，走100次
					authors = self.conf_authorlist[conf]
					numa = len(authors)#numa代表该会议122的作者人数38
					authorid = random.randrange(numa)#将作者顺序打乱authorid=随机数28每次都不一样，但是为38中的一个数字
            		#authorid = 28
           	 		#randrange() 方法返回指定递增基数集合中的一个随机数，基数缺省值为1。
					author = authors[authorid] #随机authorid的作者编号='33491' #将打乱的作者重新放入author
					outline += " " + self.id_author[author]#将会议名称和作者名称以空格连接{'vADB' 'aJ.Maguire'}
					confs = self.author_conflist[author]#作者对应的会议
					numc = len(confs)
					confid = random.randrange(numc)
					conf = confs[confid]
					outline += " " + self.id_conf[conf]#outline={'vADB aJ.Maguire vADB'}
				outfile.write(outline + "\n")# 产生AVAVAVA的序列。产生多个AVAVA的序列。
		outfile.close()
'''
最后的结果类似：vADB aArieSegev vADB aAlejandroP.Buchmann vADB aHeinrichJasper vADB
vSWDB aIoanaManolescu vWWW aDionysiosKostoulas vWWW aWernerRetschitzegger vKyotoInternationalConferenceonDigitalLibraries aHorstEidenberger vDELOSConference aCostantinoGrana vDELOSConference aNicolaFerro vIRCDL aTizianaCatarci vADL aSteceyE.Polonkey vADL aNaphtaliRishe vCIKM aXueLi vAPWeb aHaiZhuge vAPWeb aQingPingTan vAPWeb aKeunHoRyu vDASFAA aKuniakiUehara vDASFAA aRonSacks-Davis vSIGMODRecord aShashiK.Gadia vVLDB aSudarshanS.Chawathe vVLDB
形式为VAVAVA.
'''
#python py4genMetaPaths.py 1000 100 net_aminer output.aminer.w1000.l100.txt
#python py4genMetaPaths.py 1000 100 net_dbis   output.dbis.w1000.l100.txt

#dirpath = "net_aminer"
# OR 
#dirpath = "net_dbis"


numwalks = 5
walklength = 2

dirpath = "E:\\#study\\Experiment\\(metapath2vec)\\data\\net_dbis"
outfilename = "E:\\#study\\Experiment\\(metapath2vec)\\data\\net_dbis\\output.txt"
def main():
	mpg = MetaPathGenerator()
	mpg.read_data(dirpath)
	mpg.generate_random_aca(outfilename, numwalks, walklength)


if __name__ == "__main__":
	main()






























