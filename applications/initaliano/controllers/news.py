# coding: utf8

from gluon.tools import Crud
crud = Crud(db)

def index():
    news = db().select(db.i_news.ALL)
    return dict(news=news)

def create():
    return dict(form=crud.create(db.i_news))

def show():
    return dict(item=crud.read(db.i_news, request.args(0)))

def update():
    return dict(item=crud.update(db.i_news, request.args(0)))

def download():
    return response.download(request, db)
