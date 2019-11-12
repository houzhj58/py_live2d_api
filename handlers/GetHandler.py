# -*- coding: utf8 -*-

class GetHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        try:
            #获取参数id的值 
            arg_id = self.get_argument("id", "2-47")
            if arg_id is None:
                raise Exception("id is Wrong")
            model_info = arg_id.split("-")
            if len(model_info) != 2:
                raise Exception("The Format of id is XX-XX ")
            
            modelId = (int)(model_info[0])
            modelTexturesId = (int)(model_info[1])
            
            model_lst = modelList()
            model_textures = modelTextures()
            #获取模型对应的名称
            modelName = model_lst.id_to_name(modelId)
            index_json = {}
            if type(modelName) == list:
                """类似于这种  ["ShizukuTalk/shizuku-48",  "ShizukuTalk/shizuku-pajama"]"""
                if modelTexturesId > 0:
                    modelName = modelName[modelTexturesId -1]
                else:
                    modelName = modelName[0]
                index_json_file = 'model/' + modelName + '/index.json'
                with open(index_json_file, "r") as f:
                    index_json = json.load(f)
            else:
                """类似于这种  "bilibili-live/22"   """
                index_json_file = 'model/' + modelName + '/index.json'
                with open(index_json_file, "r") as f:
                    index_json = json.load(f)
                if modelTexturesId > 0:
                    modelTexturesName = model_textures .get_name(modelName, modelTexturesId)
                    index_json['textures'] = modelTexturesName
            if "model" in index_json:
                index_json['model'] = 'model/' + modelName  + '/' + index_json['model']
            if "pose" in index_json:
                index_json['pose'] = 'model/' + modelName + '/' + index_json['pose']
            if "physics" in index_json:
                index_json['physics'] = 'model/' + modelName + '/' + index_json['physics']
            
            textures = json.dumps(index_json['textures'])
            textures = textures.replace('texture', 'model/' + modelName + '/texture')
            textures = json.loads(textures)
            index_json['textures'] = textures

            if "motions" in index_json:
                motions = json.dumps(index_json['motions'])
                motions = motions.replace('sounds', 'model/'+ modelName + '/sounds')
                motions = motions.replace('motions', 'model/' + modelName + '/motions')
                motions = json.loads(motions,)
                index_json['motions'] = motions

            if "expressions" in index_json:
                expressions = json.dumps( index_json['expressions'])
                expressions = expressions.replace('expressions', 'model/' + modelName + '/expressions')
                expressions = json.loads(expressions)
                index_json['expressions'] = expressions

            #header("Content-type: application/json");
            #echo $jsonCompatible->json_encode($index_json);    
            #rtn = {}
            index_json['code']  = 0
            index_json['info']  = "success"

        except Exception as e:
            index_json['code']  = -1
            index_json['info']  = "error : {}".format(e)
            logging.info(e)
        finally:
            jsonstr = json.dumps(index_json, ensure_ascii=False)
            self.write(jsonstr)
            self.finish()