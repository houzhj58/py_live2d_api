# -*- coding: utf8 -*-
import os
import json

class modelTextures:
    
    #获取材质列表
    def get_textures(self, modelName):
        #读取材质组合规则
        order_json_file = 'model/' + modelName + '/textures_order.json'
        if  os.path.exists(order_json_file):                   
            $tmp = array(); 

            foreach (json_decode(file_get_contents('../model/'.$modelName.'/textures_order.json'), 1) as $k => $v) {
                $tmp2 = array(); 
                foreach ($v as $textures_dir) {
                    $tmp3 = array(); 
                    foreach (glob('../model/'.$modelName.'/'.$textures_dir.'/*') as $n => $m) $tmp3['merge'.$n] = str_replace('../model/'.$modelName.'/', '', $m);
                        $tmp2 = array_merge_recursive($tmp2, $tmp3);   
                }
                foreach ($tmp2 as $v4) $tmp4[$k][] = str_replace('\/', '/', json_encode($v4));
                $tmp = self::array_exhaustive($tmp, $tmp4[$k]);                                                                    }
            foreach ($tmp as $v) $textures[] = json_decode('['.$v.']', 1); return $textures;
        } else {
            foreach (glob('../model/'.$modelName.'/textures/*') as $v)
                $textures[] = str_replace('../model/'.$modelName.'/', '', $v);
            return empty($textures) ? null : $textures;
        }
    }

    #获取列表缓存
    def get_list(self, modelName):
        cache_file = 'model/' + modelName + '/textures.cache'
        if ( os.path.exists(cache_file) ) {

            textures = json.load(cache_file)
        else:
            textures = self.get_textures(modelName)
            if (!empty($textures)) file_put_contents('../model/'.$modelName.'/textures.cache', str_replace('\/', '/', json_encode($textures)));
        return isset($textures) ? array('textures' => $textures) : false;

    #获取材质名称
    def get_name(self, modelName, id):
        $list = self::get_list($modelName);
        return $list['textures'][(int)$id-1];
    }
    
    
    
    
    
    #数组穷举合并
    def array_exhaustive(self, arr1, arr2):
        foreach ($arr2 as $k => $v) {
            if (empty($arr1)) $out[] = $v;
            else foreach ($arr1 as $k2 => $v2) $out[] = str_replace('"["', '","', str_replace('"]"', '","', $v2.$v));
        } return $out;