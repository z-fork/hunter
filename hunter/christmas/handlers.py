# -*- coding: utf-8 -*-

import random
import logging

import tornado.web
import tornado.gen
import tornado.concurrent

from hunter.base.handlers import BaseHandler
from hunter.christmas.forms import GiftForm
from hunter.christmas.consts import COMMENTS

logger = logging.getLogger(__name__)


class ChristmasGiftHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    def initialize(self):
        super(ChristmasGiftHandler, self).initialize()
        self.template_name = 'christmas/gift.html'

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        form = GiftForm()
        self.render(self.template_name, {'form': form})

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        form = GiftForm(self.request.arguments)
        if form.validate():
            result = yield self.form_valid(form)
            self.render('christmas/outcome.html', {'obj': result})
            return
        self.form_invalid(form)

    @tornado.gen.coroutine
    def form_valid(self, form):
        name = form.name.data
        # TODO maybe use namedtuple
        comment = random.choice(COMMENTS)
        result = {
            'name': name,
            'comment': comment[0],
            'comment_img': comment[1]
        }
        raise tornado.gen.Return(result)

    def form_invalid(self, form):
        context = {'form': form}
        self.add_additional_context(context)
        self.render(self.template_name, context)
