pupʵ�鲽��
1 ִ��genMetaPath.py�ļ�
������numwalks�� walklength
���룺
id_user.txt(�û�id���������У�\t�ָ�[��ʱ����id��ʾ])
id_poi.txt(�û�poi���������У�\t�ָ�[��ʱ����id��ʾ])
user_poi(�û�ǩ�������У�\t�ָ�[��ʱ����id��ʾ])
�����
random_walks.txt��Ԫ·��������pupup...��id��ʾp��u��
·���޸ģ�
dirpath��newoutfilename

2 ִ��dealdata.py�ļ�
���룺
random_walks.txt
�����
node_type.txt��δȥ�أ��ִʣ���עʵ�����ͣ�
node_type_mapings.txt��ȥ�أ�
·���޸ģ�
xieleibie()����������·����quchong()����������·��

3 ִ��main.py�ļ�
���룺
random_walks.txt
node_type_mapings.txt
�����
log�ļ�������Ƕ������
·���޸ģ�--walks��--types��--log
�ڲ����������޸ģ�
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

4 ִ��vec2csv.py�ļ�
���루��log�ļ����
index2nodeid.json
node_embeddings.npz
node_type_mapings.txt(��ȡp��u��id�б�)
poi_cate_index.txt(��ȡpoi�����������б�)
�����
csv�ļ�����poi���������������
·���޸ģ�json.load��np.load��readnodetype()��һ����poi_category()��һ����data2csv��һ��