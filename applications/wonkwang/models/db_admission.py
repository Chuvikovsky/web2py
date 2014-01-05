# -*- coding: utf-8 -*-

sex_dict = {'m':T('men'), 'f':T('female')}
sex_dict_ru = {'женский':'f', 'мужской': 'm'}

def hash_generator():
    import random
    hash_str = ''
    for i in range(6):
        hash_str += random.choice('0123456789abcdefABCDEF')
    return hash_str

db.define_table('groups',
    Field('name', 'string', required=True), # пример: 2-1
    Field('letter', 'string'), # А
    Field('weekdays', 'string'), # Вт-Чт
    Field('hours', 'string'), # 19:00~20:30
    Field('comments', 'string') # 2 раза в неделю
)

db.define_table('wkform',
# фамилия
    Field('surname', 'string', length=125, label=T('Surname')),
# имя
    Field('name', 'string', length=125, label=T('Name')),
# отчество
    Field('middlename', 'string', length=125, label=T('Middlename')),
# дата рождения
    Field('birth_date', 'string', length=125, label=T('Birth date')),
# пол
    Field('sex', 'string', length=1, label=T('Sex')),
# гражданство
    Field('citizenship', 'string', length=125, label=T('Citizenship')),
# номер паспорта
    Field('passport_number', 'string', length=125, label=T('Passport')),
# домашний телефон
    Field('house_phone', 'string', length=125, label=T('House phone')),
# мобильный телефон
    Field('mobile_phone', 'string', length=125, label=T('Mobile phone')),
# email
    Field('email', 'string', length=125, label=T('Email')),
# адрес
    Field('address', 'string', length=512, label=T('Address')),
# место учебы или работы
    Field('academic', 'string', length=512, label=T('Academic')),
# специальность или должность
    Field('speciality', 'string', length=512, label=T('Speciality')),
# дни и время занятий
#    Field('group_id', 'reference groups', label=T('Group'), requires = IS_IN_DB(db,db.groups.id,'%(name)s %(weekdays)s %(hours)s'), widget=SQLFORM.widgets.options.widget),
# название группы из анкеты (2-1, например)
    Field('group_name', 'string', length=125, label=T('Group name')),
# доп. информация по группе из анкеты (Вт-Чт 18:00~19:00, например)
    Field('group_info', 'string', length=125, label=T('Group info')),
# почему корейский
    Field('why_korean', 'text', label=T('Why korean')),
# дата заполнения
    Field('completed', 'datetime', label=T('Completed')),
#hash
    Field('str_hash', 'string', readable=False, writable=False, label=T('Hash'))
)