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
from model_list import modelList

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
            
            modelId = (int)model_info[0]
            modelTexturesId = (int)model_info[1]
            
            model_lst = modelList()
            #获取模型对应的名称
            modelName = model_lst.id_to_name(modelId)

            if type(modelName) == list:
                if modelTexturesId > 0:
                    modelName = modelName[modelTexturesId -1]
                else:
                    modelName = modelName[0]
                index_json_file = '../model/' + modelName + '/index.json'
                index_json = json.load(index_json_file)
            else:
                index_json_file = '../model/' + modelName + '/index.json'
                index_json = json.load(index_json_file)
                if modelTexturesId > 0:
                    modelTexturesName = modelTextures->get_name($modelName, $modelTexturesId);
        if (isset($modelTexturesName)) $json['textures'] = is_array($modelTexturesName) ? $modelTexturesName : array($modelTexturesName);
    }
}

$textures = json_encode($json['textures']);
$textures = str_replace('texture', '../model/'.$modelName.'/texture', $textures);
$textures = json_decode($textures, 1);
$json['textures'] = $textures;

$json['model'] = '../model/'.$modelName.'/'.$json['model'];
if (isset($json['pose'])) $json['pose'] = '../model/'.$modelName.'/'.$json['pose'];
if (isset($json['physics'])) $json['physics'] = '../model/'.$modelName.'/'.$json['physics'];

if (isset($json['motions'])) {
    $motions = json_encode($json['motions']);
    $motions = str_replace('sounds', '../model/'.$modelName.'/sounds', $motions);
    $motions = str_replace('motions', '../model/'.$modelName.'/motions', $motions);
    $motions = json_decode($motions, 1);
    $json['motions'] = $motions;
}

if (isset($json['expressions'])) {
    $expressions = json_encode($json['expressions']);
    $expressions = str_replace('expressions', '../model/'.$modelName.'/expressions', $expressions);
    $expressions = json_decode($expressions, 1);
    $json['expressions'] = $expressions;
}

header("Content-type: application/json");
echo $jsonCompatible->json_encode($json);



            
            rtn = {}
            rtn['code']  = 0
            rtn['info']  = "success"
            
            rtn['result'] = mongo_op.get_task_result(task_id, result_type)


        except Exception as e:
            rtn['code']  = -1
            rtn['info']  = "error : {}".format(e)
            logging.info(e)
        finally:
            jsonstr = json.dumps(rtn, ensure_ascii=False)
            if cb is not None:
                self.write(cb + "(" + jsonstr + ")")
            else:
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
            (r"/add", AddHandler),
            (r"/get", GetHandler),
            (r"/rand", RandHandler),
            (r"/switch", SwitchHandler),
            (r"/rand_textures", RandTexturesHandler),
            (r"/switch_textures", SwitchTexturesHandler),
            (r"/(favicon\.ico)", tornado.web.StaticFileHandler, dict(path=settings['static_path']))],
            manager=manager,mongo_op = mongo_op,kernel_url=kernel_url,kernel_port=kernel_port,kernel_list = kernel_list,max_num = max_num ,time_out = time_out,rt_flag = rt_flag,**settings)
    
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    
    tornado.ioloop.IOLoop.instance().start()