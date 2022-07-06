import os 
import json



class Extractor():
    
    def __init__(self, version, num_class) -> None:
        
        self.version = version.replace('.', '-')
        self.dataset_path = os.getcwd() + '/dataset' + f'/{self.version}'
        self.dataset_json_path = self.dataset_path + f'/activity_net.v{self.version}.min.json'
        self.num_classes = num_class
        content = json.load(open(self.dataset_json_path))
        # database : dictionary 
        # key : file name without extension
        # --- value ---
        # annotaions - (list of annotation dictionary)
        #   a annotation dictionary has two pair (label, labelstring), (segment, [start,end])
        # duration
        # resolution
        # subset
        # url
        self.database = content['database'] #dictionary 
        # taxomomy : list of dictionary
        # {
        # 'nodeId': 68, 
        # 'nodeName': 'Drinking coffee', 
        # 'parentId': 46,
        # 'parentName': 'Eating and Drinking'}
        self.taxonomy = content['taxonomy'] 
        self.version = content['version'] # string
        self.list_label = self.get_list_label()
        self.dict_label_cnt = self.get_sorted_dict_label_cnt()
        self.list_top_n_label = list(self.dict_label_cnt.keys())[:num_class]
        self.dict_top_n_label_videos = self.get_dict_top_n_label_videos()    

    def get_list_label(self):
        leaf_nodes_list = self.get_leaf_nodes()
        list_label = [data['nodeName'] for data in leaf_nodes_list]
        return list_label

    def get_leaf_nodes(self):
        all_node_ids = [data["nodeId"] for data in self.taxonomy]
        leaf_node_ids = []
        for x in all_node_ids:
            is_parent = False
            for query_node in self.taxonomy:
                if query_node["parentId"]==x: is_parent = True
            if not is_parent: leaf_node_ids.append(x)
        leaf_nodes = [x for x in self.taxonomy if x["nodeId"] in  leaf_node_ids]
        return leaf_nodes

    def get_sorted_dict_label_cnt(self):
        dict_label_cnt = { label : 0 for label in self.get_list_label()}
        for key in self.database:
            annotations, duration, resolution, subset, url = self.database[key].values()
            for annotaion in annotations:
                label = annotaion['label']
                # segment = annotaion['segment']
                dict_label_cnt[label] += 1

        dict_label_cnt_sorted = {k : v for k, v in sorted(dict_label_cnt.items(), key = lambda item : item[1], reverse=True)}
        return dict_label_cnt_sorted

    def get_dict_top_n_label_videos(self,sort = False):
        dict_n_label_videos = { label: [] for label in  self.list_top_n_label}
        for video_name in self.database:
            annotations, duration, resolution, subset, url = self.database[video_name].values()
            for annotaion in annotations:
                label = annotaion['label']
                if label in self.list_top_n_label:
                    dict_n_label_videos[label].append(video_name)
        # 라벨별 비디오 키값 제거
        for label in self.list_top_n_label:
            dict_n_label_videos[label] = list(set(dict_n_label_videos[label]))
        
        # if sort:
        #     dict_n_label_videos_sorted = {k : v for k, v in sorted(dict_n_label_videos.items(), key = lambda item : len(item[1]), reverse=True)}
        #     return dict_n_label_videos_sorted
        
        return dict_n_label_videos



