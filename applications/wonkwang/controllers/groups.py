# -*- coding: utf-8 -*-
# manage groups for wonkwang form

crud.settings.create_next = URL('index')
crud.settings.update_next = URL('index')
crud.settings.delete_next = URL('index')
crud.settings.showid = False

def index():
    rows = SQLTABLE(db().select(db.groups.ALL), linkto=lambda field,type,ref: URL('update', args=field))
    return dict(rows=rows)

def create():
    return dict(form=crud.create(db.groups))

def update():
    return dict(form=crud.update(db.groups, request.args(0)))

def delete():
    return dict(form=crud.delete(db.groups, request.args(0)), message='Record '+str(request.args(0))+' deleted')
