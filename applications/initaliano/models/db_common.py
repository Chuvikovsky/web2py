# coding: utf8

db.define_table('i_level',
    Field('name_en','string', length=256, required=True),
    Field('name_ru', 'string', length=512, required=True)
)

db.i_level.name_en.requires = IS_NOT_EMPTY()
db.i_level.name_ru.requires = IS_NOT_EMPTY()