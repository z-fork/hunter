# -*- coding: utf-8 -*-

import time
import signal
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options
from hunter.settings import settings
from urls import url_patterns


class HunterApp(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        # db = connect_mongo(MONGODB, **kwargs)
        super(HunterApp, self).__init__(
            url_patterns, *args, **dict(settings, **kwargs))


def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    logging.info('Stopping http server')
    http_server.stop()  # 不接收新的 HTTP 请求

    logging.info('Will shutdown in %s seconds ...', settings['MAX_WAIT_SECONDS_BEFORE_SHUTDOWN'])
    deadline = time.time() + settings['MAX_WAIT_SECONDS_BEFORE_SHUTDOWN']

    def stop_loop():
        now = time.time()
        io_loop = tornado.ioloop.IOLoop.instance()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()  # 处理完现有的 callback 和 timeout 后，可以跳出 io_loop.start() 里的循环
            logging.info('Shutdown')
    stop_loop()

if __name__ == "__main__":
    app = HunterApp()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    tornado.ioloop.IOLoop.instance().start()
