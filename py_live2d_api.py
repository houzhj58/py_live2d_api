# -*- coding: utf8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
import tornado.httpclient
import os,sys
import json
import time,datetime
import signal
import logging
from logging.handlers import RotatingFileHandler
from tornado.options import define, options
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.options import options, parse_command_line, define
from tornado.escape import json_encode, json_decode, url_escape
import copy
from modelList import modelList
from modelTextures import modelTextures

define("port", default=1234, help="run on the given port", type=int)
define("file", default="config.yml", help="run on the given file", type=str)

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

class RandHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        try:
            
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
class SwitchHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        try:
            
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
class RandTexturesHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        try:
            
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
class SwitchTexturesHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        try:
            
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

if __name__ == "__main__":
    tornado.options.parse_command_line()
    logging.info("web:recommend port %d start" % options.port)

    #/add/ - 检测 新增皮肤 并更新 缓存列表
    #/get/?id=1-23 获取 分组 1 的 第 23 号 皮肤
    #/rand/?id=1 根据 上一分组 随机切换
    #/switch/?id=1 根据 上一分组 顺序切换
    #/rand_textures/?id=1-23 根据 上一皮肤 随机切换 同分组其他皮肤
    #/switch_textures/?id=1-23 根据 上一皮肤 顺序切换 同分组其他皮肤
    app = tornado.web.Application(
    handlers=[
            ("/add", AddHandler),
            ("/get", GetHandler),
            ("/rand", RandHandler),
            ("/switch", SwitchHandler),
            ("/rand_textures", RandTexturesHandler),
            ("/switch_textures", SwitchTexturesHandler),
            #(r"/(favicon\.ico)", tornado.web.StaticFileHandler, dict(path=settings['static_path']))],
            ]
    )
    
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    #signal.signal(signal.SIGTERM, sig_handler)
    #signal.signal(signal.SIGINT, sig_handler)
    
    tornado.ioloop.IOLoop.instance().start()