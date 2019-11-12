# -*- coding: utf8 -*-

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