# coding: utf8

db.define_table('i_reading',
    Field('name_it', 'string', length=256, required=True),
    Field('name_ru', 'string', length=256),
    Field('author', 'string', length=512,),
    Field('work_by', 'string', length=256),
    Field('audio', 'upload', uploadfolder=os.path.join(request.folder, 'uploads/mp3')),
    Field('text_it', 'text', required=True),
    Field('text_ru', 'text'),
    Field('created_at', 'datetime'),
    Field('updated_at', 'datetime', compute=lambda row: datetime.datetime.now())
)

db.i_reading.name_it.requires = IS_NOT_EMPTY()
db.i_reading.text_it.requires = IS_NOT_EMPTY()