import json
import os
import sys
import matplotlib.pyplot as plt
from lib_extract import Extractor

try:
    if len(sys.argv) != 3:
        raise Exception()
    version = sys.argv[1]
    version = str(version)
    num_classes = sys.argv[2]
    num_classes = int(num_classes)
    
    
except:
    print(f'usage : python3 <version of activitynet dataset (1.2 or 1.3)> <number of top classes to be extracted>')
    exit()
    
DATASET_VERSION = '1-2' if version == 1.2 else '1-3'

def make_top_n_label_info_file(dict_n_label_videos, dataset_version):
    f = open(f'top {len(dict_n_label_videos)} labels metadata_{dataset_version}.txt', 'w')
    for key,val in dict_n_label_videos.items():
        line = key + ' ' + str(len(val)) + '\n'
        print(line)
        f.write(line)
    f.write('\n')    
    for key,val in dict_n_label_videos.items():
        line = key + '\n'
        f.write(line)
        line = ','.join(val) + '\n'
        f.write(line)
    f.close()

def check_label_cnt_label_video_len(list_top_n_label,dict_n_label_videos,dict_label_cnt_sorted):
    for label in list_top_n_label:
        print(f'label : {label}, # annotaion : {dict_label_cnt_sorted[label]} # video : {len(dict_n_label_videos[label])} ')
        # if len(dict_n_label_videos[label]) != dict_label_cnt_sorted[label]:
            # raise Exception(f'number of videos that have top N label is wrong')

def make_bar_chart(list_top_n_label, dict_n_label_videos):
    values = [len(dict_n_label_videos[label]) for label in list_top_n_label]
    plt.bar(list_top_n_label, values)
    for i in range(len(list_top_n_label)): plt.text(i,values[i],values[i], ha ='center')
    plt.show()


if __name__ == "__main__":
    
    extractor = Extractor(DATASET_VERSION, num_classes)
    list_label = extractor.list_label
    dict_label_cnt = extractor.get_sorted_dict_label_cnt() # 전체 어노테이션에서 label이 나온 횟수

    list_top_n_label = list(dict_label_cnt.keys())[:num_classes] # 전체 어노테이션에서 label 많이 나온 경우 ( 비디오 개수보다 많음)
    dict_n_label_videos = extractor.get_dict_top_n_label_videos() # 가장 많이 나온 라벨들에 해당하는 비디오 이름 

    make_top_n_label_info_file(dict_n_label_videos, version)    
    make_bar_chart(list_top_n_label, dict_n_label_videos)

