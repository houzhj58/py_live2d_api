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