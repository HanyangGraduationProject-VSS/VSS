import os
import sys

from lib_extract import Extractor


def read_metadata(dir_elements):
    dir_elements = os.listdir(os.getcwd())
    valid = False
    idx = 0
    for i  in range(len(dir_elements)):
        if f'top {NUM_CLASS} labels' in dir_elements[i]:
            idx = i
            valid = True
            break
    if not valid: 
        raise Exception("extract top n classes first using n_class_extrator.py")

    with open(dir_elements[idx]) as metadata:
        lines = metadata.readlines()[NUM_CLASS+1:]
    return lines

# N 개의 클래스와 그에 해당하는 비디오 이름을 얻어옵니다. 
# 어떤 형태로든 읽어옵니다.

# read N class and video names

try:
    if len(sys.argv) != 3:
        raise Exception()
    DATASET_VERSION = sys.argv[1]
    NUM_CLASS = sys.argv[2]
    DATASET_VERSION = str(DATASET_VERSION)
    NUM_CLASS = int(NUM_CLASS)
except:
    print(f'usage : python3 <version of activitynet dataset (1.2 or 1.3)> <number of top classes to be loaded>')
    exit()

dir_elements = os.listdir(os.getcwd())
lines = read_metadata(dir_elements)

dict_top_n_label_video = {}
for i in range(len(lines)):
    if i % 2 == 1:
        line = lines[i]
        dict_top_n_label_video[lines[i-1].strip('\n')] = line.strip('\n').split(',')

extractor = Extractor(DATASET_VERSION, NUM_CLASS)

for label in dict_top_n_label_video.keys():
    videos = dict_top_n_label_video[label]
    for video in videos:
        final_path = extractor.dataset_path + f"/{extractor.database[video]['subset']}/{video}"
        final_path = final_path.replace('training','train')
        final_path = final_path.replace('validation','val')
        final_path = final_path.replace('testing','test')
        print(final_path)

# 읽어들이는 최종 링크 



