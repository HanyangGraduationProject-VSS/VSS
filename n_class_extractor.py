import json
import os
import sys

version = sys.argv[1]
num_classes = sys.argv[2]



try:
    if len(sys.argv) != 3:
        raise Exception()
    version = float(version)
    num_classes = int(num_classes)
except:
    print(f'usage : python3 <version of activitynet dataset (1.2 or 1.3)> <number of top classes to be extracted>')
    exit()
    


dataset_version = '1-2' if version == 1.2 else '1-3'

def get_json_content(version):
    project_root_path = os.getcwd()
    dataset_dir_path = project_root_path + '/dataset' + f'/{version}'
    dataset_json_path = dataset_dir_path + f'/activity_net.v{version}.min.json'
    file_dataset_json = open(dataset_json_path)
    dataset_json_content = json.load(file_dataset_json)
    return dataset_json_content

def get_leaf_nodes(taxonomy):
    all_node_ids = [data["nodeId"] for data in taxonomy]
    leaf_node_ids = []
    for x in all_node_ids:
        is_parent = False
        for query_node in taxonomy:
            if query_node["parentId"]==x: is_parent = True
        if not is_parent: leaf_node_ids.append(x)
    leaf_nodes = [x for x in taxonomy if x["nodeId"] in  leaf_node_ids]
    return leaf_nodes

def get_dict_label_cnt(list_label):
    dict_label_cnt = { label : 0 for label in list_label}
    for key in database:
        annotations, duration, resolution, subset, url = database[key].values()
        for annotaion in annotations:
            label = annotaion['label']
            # segment = annotaion['segment']
            dict_label_cnt[label] += 1
    return dict_label_cnt

def get_dict_n_label_videos(list_top_n_label):
    dict_n_label_videos = { label: [] for label in  list_top_n_label}
    for key in database:
        annotations, duration, resolution, subset, url = database[key].values()
        for annotaion in annotations:
            label = annotaion['label']
            if label in list_top_n_label:
                dict_n_label_videos[label].append(key)
    return dict_n_label_videos
def check_label_cnt_label_video_len(list_top_n_label,dict_n_label_videos,dict_label_cnt_sorted):
    for label in list_top_n_label:
        if len(dict_n_label_videos[label]) != dict_label_cnt_sorted[label]:
            raise Exception(f'number of videos that have top N label is wrong')

        

json_content = get_json_content(dataset_version)
# database : dictionary 
# key : file name without extension
# --- value ---
# annotaions - (list of annotation dictionary)
#   a annotation dictionary has two pair (label, labelstring), (segment, [start,end])
# duration
# resolution
# subset
# url

database = json_content['database'] #dictionary 
# taxomomy : list of dictionary
# {
# 'nodeId': 68, 
# 'nodeName': 'Drinking coffee', 
# 'parentId': 46,
# 'parentName': 'Eating and Drinking'}
taxonomy = json_content['taxonomy'] 

# version = json_content['version'] # string
# 1. 라벨 리스트를 만든다. 2. 라벨을 키로 사용하는 딕셔너리를 만든다.
# 3. json을 뒤지면서 라벨의 밸류를 늘려준다. 

leaf_nodes_list = get_leaf_nodes(taxonomy)
list_label = [data['nodeName'] for data in leaf_nodes_list]
dict_label_cnt = get_dict_label_cnt(list_label)

dict_label_cnt_sorted = {k : v for k, v in sorted(dict_label_cnt.items(), key = lambda item : item[1], reverse=True)}
list_top_n_label = list(dict_label_cnt_sorted.keys())[:num_classes]
dict_n_label_videos = get_dict_n_label_videos(list_top_n_label)
check_label_cnt_label_video_len(list_top_n_label,dict_n_label_videos,dict_label_cnt_sorted)

# 라벨과 그 개수 필요
# for label in list_top_n_label:
#     # print(label,dict_label_cnt_sorted[label] , dict_n_label_videos[label])
#     print(label,dict_label_cnt_sorted[label])

# 이걸 파일 형태로 짜잔하고 저장한다음에 시각화해보자.  #아그런데 서브셋도 표기해얗

for videos in dict_n_label_videos.values():
    for video in videos:
        print(database[video]['subset'])


# 최종적으로 필요한거: 클래스 이름, 비디오 개수와 이름, 서브셋