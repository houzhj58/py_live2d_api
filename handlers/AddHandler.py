# -*- coding: utf8 -*-

class AddHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        try:
            rtn = {}
            ml = modelList()
            mt =modelTextures()

            model_lst = ml.get_list()
            model_lst = model_lst['models']

            echo = list()
            for model_name in model_lst:
                if type(model_name) == list:
                    continue
                else:
                    cache_file_path = 'model/' + model_name + '/textures.cache'
                    if os.path.exists(cache_file_path):
                        textures = list()
                        textures_new = list()
                        model_textures_lst = mt.get_list(model_name)
                        model_name_textures = mt.get_textures(model_name)
                        if type(model_textures_lst['textures']) is list:
                            for texture in model_textures_lst['textures']:
                                if type(texture) is list:
                                    for tex in texture:
                                        textures.append( tex.replace('\/', '/') )
                                else:
                                    textures.append( texture.replace('\/', '/') )
                        if len(textures) == 0:
                            continue
                        if type(model_name_textures) is list:
                            for texture in model_name_textures:
                                textures_new.append( texture.replace("\/", '/' ))
                        textures_diff = list( set( textures_new).difference(set(textures)))
                        if len(textures_diff) == 0:
                            echo.append(  model_name +  ' / textures.cache / No Update.')
                        else:
                            pass
                            #foreach (array_values(array_unique(array_merge($textures, $texturesNew))) as $v) $texturesMerge[] = json_decode($v, 1);
                            #file_put_contents('../model/'.$modelName.'/textures.cache', str_replace('\/', '/', json_encode($texturesMerge)));
                            #echo '<p>'.$modelName.' / textures.cache / Updated.</p>';
                    else:
                        model_textures = mt.get_list(model_name)
                        echo.append(model_name + ' / textures.cache / Created.') 

            rtn['echo'] = echo
            rtn['code']  = 0
            rtn['info']  = "success"
        except Exception as e:
            rtn['code']  = -1
            rtn['info']  = "error : {}".format(e)
            logging.info(e)
        finally:
            jsonstr = json.dumps(rtn, ensure_ascii=False)
            self.write(jsonstr)
            self.finish()