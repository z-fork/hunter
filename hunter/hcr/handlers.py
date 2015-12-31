# -*- coding: utf-8 -*-

import logging

import tornado.web
import tornado.gen
import tornado.concurrent

from hunter.base.handlers import BaseHandler

logger = logging.getLogger(__name__)


class HCRHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    def initialize(self):
        super(HCRHandler, self).initialize()
        self.template_name = 'hcr/show.html'

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        self.render(self.template_name)
