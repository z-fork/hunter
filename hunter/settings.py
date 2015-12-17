import os
import logging.config
import tornado
import tornado.template
from tornado.options import define, options
from jinja2 import Environment, FileSystemLoader

# Make filepaths relative to settings.
location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)

define("port", default=8888, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")

tornado.options.parse_command_line()

STATIC_ROOT = location('static')
TEMPLATE_ROOT = location('templates')

TOKEN = 'epmbppowvmxjqm'

# Deployment Configuration
settings = {
    'debug': options.debug,
    'static_path': STATIC_ROOT,
    'cookie_secret': "vZS/c+BKTASaEjrBJ51uMMX+AwCyp0bcmXHOlX0jd0s=",
    'cookie_expires': 31,  # cookie will be valid for this amount of days
    'xsrf_cookies': True,
    'login_url': '/login/',

    'MAX_WAIT_SECONDS_BEFORE_SHUTDOWN': 10,
}

# Jinja settings
# for all options see http://jinja.pocoo.org/docs/api/#jinja2.Environment
JINJA = {
    'autoescape': True,
    'extensions': [
        'jinja2.ext.with_'
    ],
}
JINJA_ENV = Environment(loader=FileSystemLoader(TEMPLATE_ROOT), **JINJA)

MONGODB = {
    'host': '127.0.0.1',
    'port': 27017,
    'db_name': "acl_app",
    'reconnect_tries': 5,
    'reconnect_timeout': 2,  # in seconds
}

# See PEP 391 and logconfig for formatting help.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
            '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'rotate_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': location('logs/main.log'),
            'when': 'midnight',
            'interval':    1,  # day
            'backupCount': 7,
            'formatter': 'main_formatter',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
            # 'filters': ['require_local_true'],
        },
    },
    'loggers': {
        '': {
            'handlers': ['rotate_file', 'console'],
            'level': 'DEBUG',
        }
    }
}

logging.config.dictConfig(LOGGING)

if options.config:
    tornado.options.parse_config_file(options.config)
