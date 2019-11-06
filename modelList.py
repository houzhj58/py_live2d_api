# -*- coding: utf8 -*-
import json

class modelList:
    #获取模型列表
    def get_list(self):
        # 读取数据
        with open('model_list.json', 'r') as f:
            data = json.load(f)
        return data
    
    #获取模组名称
    def id_to_name(self, id):
        list = self.get_list()
        return list['models'][id-1]
    
    #转换模型名称
    def name_to_id(self, name):
        list = self.get_list()
        #$id = array_search($name, $list['models']);
        #return is_numeric($id) ? $id + 1 : false



if __name__ == "__main__":
    model_lst = modelList()
    #print (model_lst.get_list())

    name = model_lst.id_to_name(5)
    print(name)

