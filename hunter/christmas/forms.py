# -*- coding: utf-8 -*-

import logging

from wtforms import StringField, validators

from hunter.base.forms import Form


logger = logging.getLogger(__name__)


class GiftForm(Form):
    name = StringField('name', [validators.InputRequired()])

    text_errors = {
        'not_found': 'name mismatch',
    }
