import os
import json
import pandas as pd
from torch.utils.data import Dataset
from torchvision.io import read_video


def get_file_fullnames_in_dir(dirname):
    filenames = os.listdir(dirname)
    res = []
    for filename in filenames:
        fullname = os.path.join(dirname,filename)
        res.append(fullname)
    return res

root = os.getcwd() + '/dataset'
path_train =  root + '/train/'
path_test = root + '/test/'
path_valid = root + '/val/'
path_json = root + '/activity_net.v1-2.min.json'


'''
데이터 : 비디오 이름, annotation 
'''

def get_train_dataset():
    pass

def get_test_dataset():
    pass

def get_valid_dataset():
    pass

def make_dataset( path_json):

    train_videodata_list, test_videodata_list, valid_videodata_list = [],[],[]

    json_content = json.load(open(path_json))
    database = json_content['database'] #dictionary 
    taxonomy = json_content['taxonomy'] #list
    version = json_content['version'] # string
    # csv 에서 추출한 database를 dataframe으로 전환합니다.
    database = pd.DataFrame(database).T
    
    # query = 'subset == {}'.format('training')
    for set_type in ("training","testing","validation")[:1]:
        # 해당 서브셋에 대한 dataframe
        subset = database.query(f'subset == "{set_type}"')
        for idx in subset.index.values[:1]:
            data = subset.loc[idx] 
            annotations = data['annotations']
            duration = data['duration']
            videoData = VideoData(id = idx, annotations=annotations,duration =duration)
            if set_type == "training":
                train_videodata_list.append(videoData)
            elif set_type == "testing":
                test_videodata_list.append(videoData)
            else :
                valid_videodata_list.append(videoData)
    
    return VideoDataset(train_videodata_list,set_type),VideoDataset(test_videodata_list,set_type), VideoDataset(valid_videodata_list,set_type)


make_dataset(path_json)


# 텐서, 아이디, 어노테이션, 서브셋 순으로 (final )
class VideoDataset(Dataset):
    def __init__(self, datalist, set_type) -> None:
        self.datalist = datalist
        self.datalist = set_type
    def __len__(self):
        return len(self.datalist)
    def __getitem__(self, index) :
        # 텐서, 아이디, 어노테이션, 서브셋 순으로 
        if 데이터리스트 타입에 따라서 텐서로 변경하여 리턴해준다.:
        return self.datalist[index]


# 텐서, 라벨
class VideoData:
    def __init__(self, video_id, annotations,subset) -> None:
        self.video_id = video_id
        self.annotaions = annotations
        self.subset = subset

class annotation:
    def __init__(self, label, segment) -> None:
        self.label = label
        self.segment = segment



