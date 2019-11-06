# -*- coding: utf8 -*-
import os
import json
import glob

class modelTextures:
    
    #获取材质列表
    def get_textures(self, modelName):
        #读取材质组合规则
        order_json_file = 'model/' + modelName + '/textures_order.json'
        textures = list()
        if  os.path.exists(order_json_file):
            pass
            """with open(order_json_file, "r") as f:
                order_json = json.load(f)
            
            tmp = list()
            for key, value in order_json.item():
                tmp2 = list()     
                foreach ($v as $textures_dir) {
                    $tmp3 = array(); 
                    foreach (glob('../model/'.$modelName.'/'.$textures_dir.'/*') as $n => $m) $tmp3['merge'.$n] = str_replace('../model/'.$modelName.'/', '', $m);
                        $tmp2 = array_merge_recursive($tmp2, $tmp3);   
                }
                foreach ($tmp2 as $v4) $tmp4[$k][] = str_replace('\/', '/', json_encode($v4));
                $tmp = self::array_exhaustive($tmp, $tmp4[$k]);                                                                    }
            foreach ($tmp as $v) $textures[] = json_decode('['.$v.']', 1); 
            return $textures;"""
        else:
            textures_path_pattern = 'model/' + modelName + '/textures/*'
            textures_paths = glob.glob(textures_path_pattern)
            for path in textures_paths:
                textures.append(  path.replace('model/' + modelName + '/', '') )
        return textures

    #获取列表缓存
    def get_list(self, modelName):
        cache_file_path = 'model/' + modelName + '/textures.cache'
        ret = {}
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'r') as f:
                textures = json.load(f)
        else:
            textures = self.get_textures(modelName)
            if textures is not None:
                textures = textures.replace("\/", "/")
                json.dump(textures, cache_file_path)
        ret["textures"] = textures
        return ret

    #获取材质名称
    def get_name(self, modelName, id):
        cache_list = self.get_list(modelName)
        return cache_list['textures'][id-1]   
    
    #数组穷举合并
    #def array_exhaustive(self, arr1, arr2):
        #foreach ($arr2 as $k => $v) {
            #if (empty($arr1)) $out[] = $v;
            #else foreach ($arr1 as $k2 => $v2) $out[] = str_replace('"["', '","', str_replace('"]"', '","', $v2.$v));
        #} return $out;




if __name__ == "__main__":
    name = "Potion-Maker/Tia"
    id = 47

    mt = modelTextures()

    name = mt.get_name(name, id)
    print(name)