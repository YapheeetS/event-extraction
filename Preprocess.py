import os
from xml.etree.ElementTree import parse
from Config import MyConfig


class PreprocessManager():
    def __init__(self):
        self.dir_list = MyConfig.raw_dir_list
        self.dir_path = MyConfig.raw_data_path

    def preprocess(self):
        '''
        Overall Iterator for whole dataset
        '''
        fnames = self.fname_search() #list of tuple (sgm file, apf.xml file)
        pass

    def fname_search(self):
        fname_list = []

        for dir in self.dir_list:
            full_path = self.dir_path.format(dir)
            flist = os.listdir(full_path)
            print(flist)



    def process_one_doc(self, path, docname):
        pass

    def parse_one_xml(self, path, docname):
        pass

    def parse_one_sgm(self, path, docname):
        pass

    def Data2Json(self):
        pass

    def next_train_data(self):
        pass

    def eval_data(self):
        pass


if __name__ == '__main__':
    man = PreprocessManager()
    man.preprocess()

