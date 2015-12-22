from tornado.web import url

# from pages.handlers import HomeHandler
# from accounts.handlers import RegisterHandler, LogoutHandler, LoginHandler
# from news.handlers import NewsListHandler, NewsCreateHandler,\
#     NewsDetailHandler, NewsDeleteHandler

from hunter.base.handlers import TimeHandler
from hunter.wechat.handlers import VerifyHandler
from hunter.christmas.handlers import ChristmasGiftHandler

url_patterns = [
    # echo
    url(r'/time', TimeHandler),

    # wechat verify
    url(r'/verify', VerifyHandler, name='verify'),

    # christmas
    url(r'/christmas', ChristmasGiftHandler, name='christmas_gift')

    # pages
    # url(r"/", HomeHandler, name="home"),
    #
    # # auth
    # url(r"/register/", RegisterHandler, name="register"),
    # url(r"/logout/", LogoutHandler, name="logout"),
    # url(r"/login/", LoginHandler, name="login"),
    #
    # # news
    # url(r"/news/", NewsListHandler, name="news_list"),
    # url(r"/news/create/", NewsCreateHandler, name="news_create"),
    # url(r"/news/detail/(?P<object_id>[0-9a-f]+)/", NewsDetailHandler,
    #     name="news_detail"),
    # url(r"/news/delete/(?P<object_id>[0-9a-f]+)/", NewsDeleteHandler,
    #     name="news_delete"),
]
