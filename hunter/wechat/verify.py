# -*- coding: utf-8 -*-

import logging
import hashlib

import tornado.web
import tornado.gen
import tornado.concurrent

from hunter.settings import TOKEN


l = logging.getLogger(__name__)


class VerifyHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    @tornado.gen.coroutine
    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echo_str = self.get_argument('echostr')
        if self._check_signature(signature, timestamp, nonce):
            self.write(echo_str)
        else:
            self.write('fail')
        self.finish()

    @classmethod
    def _check_signature(cls, signature, timestamp, nonce):
        items = [TOKEN, timestamp, nonce]
        items.sort()
        return hashlib.sha1(''.join(items)).hexdigest() == signature
