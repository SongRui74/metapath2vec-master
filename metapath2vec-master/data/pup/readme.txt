pup实验步骤
1 执行genMetaPath.py文件
参数：numwalks， walklength
输入：
id_user.txt(用户id索引，两列，\t分隔[用户id，用户id])
id_poi.txt(poi索引，两列，\t分隔[poiid，poi名称])
user_poi(用户签到，两列，\t分隔[用户id，poiid])
输出：
random_walks.txt（元路径，形如pupup...，id表示p、u）
路径修改：
dirpath、newoutfilename

2 执行dealdata.py文件
输入：
random_walks.txt
输出：
node_type.txt（未去重，分词，标注实体类型）
node_type_mapings.txt（去重）
路径修改：
xieleibie(路径)函数，quchong(路径)函数

3 执行main.py文件
输入：
random_walks.txt
node_type_mapings.txt
输出：
log文件，包含嵌入向量
路径修改：--walks，--types，--log
在参数设置中修改：
--walks
E:/#study/Experiment/data/pup/vector/random_walks.txt
--types
E:/#study/Experiment/data/pup/vector/node_type_mapings.txt
--log
./log
--negative-samples
5
--window
1
--epochs
100
--care-type
1

4 执行vec2csv.py文件
输入（在log文件里）：
index2nodeid.json
node_embeddings.npz
node_type_mapings.txt(读取p，u的id列表)
poi_cate_index.txt(读取poi和类别的索引列表)
输出：
csv文件（有poi索引、向量、类别）
路径修改：json.load，np.load，readnodetype()中一个，poi_category()中一个，data2csv中一个


upcpu实验步骤
1 执行genMetaPath.py文件
参数：numwalks， walklength
输入：
id_user.txt(用户id索引，两列，\t分隔[用户id，用户id])
id_poi.txt(poi索引，两列，\t分隔[poiid，poi名称])
id_category.txt(类别索引，两列，\t分隔[类别id，类别名称])
user_poi_cate(用户签到，四列，\t分隔[用户id，poiid，类别名称，类别id])
输出：
random_walks.txt（元路径，形如upcpu...，id表示p、u、c）
路径修改：
dirpath、newoutfilename

2 执行dealdata.py文件
输入：
random_walks.txt
输出：
node_type.txt（未去重，分词，标注实体类型）
node_type_mapings.txt（去重）
路径修改：
xieleibie(路径)函数，quchong(路径)函数

其余同上3，4，5

