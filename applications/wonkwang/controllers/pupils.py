# -*- coding: utf-8 -*-

# admin module for wonkwang.ru form

import os

bd_fields = {
    'surname': 'Фамилия ',
    'name': 'Имя ',
    'middlename': 'Отчество ',
    'birth_date': 'Дата рождения ',
    'sex': 'Пол ',
    'citizenship': 'Гражданство ',
    'passport_number': 'Номер паспорта ',
    'house_phone': 'Домашний телефон ',
    'mobile_phone': 'Номер мобильного телефона ',
    'email': 'Email ',
    'address': 'Адрес ',
    'academic': 'Место учебы или работы ',
    'speciality': 'Специальность или занимаемая должность ',
    'group_id': '',
    'group_name': '', # 3-2
    'group_info': '', # Вск 11:00~13:40
    'why_korean': 'Что побудило Вас изучать корейский язык ',
    'completed': 'Анкета заполнена ',
    'str_hash': ''}
bd_fields2 = [
    'surname',
    'name',
    'middlename',
    'birth_date',
    'sex',
    'citizenship',
    'passport_number',
    'house_phone',
    'mobile_phone',
    'email',
    'address',
    'academic',
    'speciality',
    'group',
    'why_korean',
    'completed']
bd_fields3 = [
    'Фамилия ',
    'Имя ',
    'Отчество ',
    'Дата рождения ',
    'Пол ',
    'Гражданство ',
    'Номер паспорта ',
    'Домашний телефон ',
    'Мобильный телефон',
#   'Номер мобильного телефона ',
    'Email ',
    'Адрес ',
    'Место учебы или работы ',
    'Специальность или занимаемая должность ',
    'Группа ',
    'Что побудило Вас изучать корейский язык ',
#    'Анкета заполнена ',
    'Учебно-образовательный центр Седжон ']

def insert():
    path_to_files = os.path.join('/Users/chuvikovsky/Documents/webdev/uploads', '1-1')
    dir_list = os.listdir(path_to_files)
    file_content_list = {}
    for item in dir_list:
        if os.path.isfile(os.path.join(path_to_files, item)):
            file_name, file_ext = os.path.splitext(item)
            if file_name in ['9e361b']:
                continue
# 36c551
            if file_ext == '.txt':
                f = open(os.path.join(path_to_files, item), 'r');
                content = ' '.join([line.strip() for line in f.readlines()])
                r = []
                for v in bd_fields3:
                    if content.split(v, 1)[0].strip() != 'None':
                        r.append(content.split(v, 1)[0].strip())
                    else:
                        r.append(' ')
                    content = content.split(v, 1)[1]
                f.close()
                file_content_list[file_name] = dict(zip(bd_fields2, r[1:]))
                group, assigned_num = file_content_list[file_name]['group'].split(' Присвоенный номер ', 1)
                group_name, group_info = group.split(' ', 1)
#                group_name, group_info = file_content_list[file_name]['group'].split(' ', 1)
                file_content_list[file_name]['group_name'] = group_name
                file_content_list[file_name]['group_info'] = group_info
                file_content_list[file_name]['str_hash'] = file_name
                file_content_list[file_name]['sex'] = sex_dict_ru[file_content_list[file_name]['sex']]
                del file_content_list[file_name]['group']
                db['wkform'].insert(**file_content_list[file_name])
    return dict(items=file_content_list)

def links_opt(row):
    if request.args(0):
        return  A('pdf', _href=URL('download', args=row.str_hash))
    else:
        return  A('pdf', _href=URL('download', args=row.wkform.str_hash))

def links_opt_id(row):
    if request.args(0):
        return  A('pdf', _href=URL('download', args=row.id))
    else:
        return  A('pdf', _href=URL('download', args=row.wkform.id))

def download():
    file_path = os.path.join(request.folder,'uploads/1-1/',str(request.args(0))+'.pdf')
    return response.stream(file_path, request=request)

def index():
    T.force('ru')
    grid = SQLFORM.grid(db.wkform)
    return dict(grid=grid)

def dublicate():
    form1 = db.wkform.with_alias('form1')
    items = db((db.wkform.id>form1.id) & (db.wkform.assigned_num==form1.assigned_num) & (db.wkform.group_id==form1.group_id)).select(
               db.wkform.id, db.wkform.surname, db.wkform.name, db.wkform.middlename, db.wkform.assigned_num, db.wkform.email, 
               form1.id, form1.surname, form1.name, form1.middlename, form1.assigned_num, form1.email,
             left=(form1.on(form1.surname==db.wkform.surname)))
    return dict(items=items)

def dublicatenames():
    response.view = 'pupils/dublicate.html'
    form1 = db.wkform.with_alias('form1')
    items = db((db.wkform.id>form1.id) & (db.wkform.name==form1.name) & (db.wkform.middlename==form1.middlename)).select(
               db.wkform.id, db.wkform.surname, db.wkform.name, db.wkform.middlename, db.wkform.assigned_num, db.wkform.email, 
               form1.id, form1.surname, form1.name, form1.middlename, form1.assigned_num, form1.email,
             left=(form1.on(form1.surname==db.wkform.surname)))
    return dict(items=items)

def report():
    T.force('ru')
    item = db((db.wkform.group_id==db.groups.id) & (db.wkform.id==request.args(0))).select().first().as_dict()
    response.title = item['wkform']['name']+' '+item['wkform']['surname']
    fields = db.wkform
    item['wkform']['group_id'] = item['groups']['name']+' ' +item['groups']['weekdays']+' ' +item['groups']['hours']

    if request.extension=="pdf":
        from gluon.contrib.pyfpdf import FPDF, HTMLMixin
        import os
        font_path = os.getcwd()+'/applications/'+request.application+'/fonts/ttf/'
        file_path = os.getcwd()+'/applications/'+request.application+'/uploads/'
        
        # create a custom class with the required functionalities 
        class MyFPDF(FPDF, HTMLMixin):
            def header(self): 
                self.add_font('DejaVu', '', font_path+'DejaVuSans.ttf', uni=True)
                self.set_font('DejaVu','',20)
                self.cell(45) # padding
                self.cell(100,10, T('Application Form').strip(),0,0,'C')
                self.ln(10)
                self.cell(155) # padding
                self.cell(30,40, T('photo').strip(),1,0,'C')
                self.ln(10)
                
            def footer(self):
                "hook to draw custom page header (printing page numbers)"
                self.set_y(-15)
                self.add_font('DejaVu', '', font_path+'DejaVuSans.ttf', uni=True)
                self.set_font('DejaVu','',15)
                #txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
                self.cell(0,10,T('about organization').strip(),0,0,'C')
                #self.write(10, ' '*20+T('about organization'))
                    
        pdf=MyFPDF()
        # create a page and serialize/render HTML objects
        pdf.add_page()
        pdf.add_font('DejaVu', '', font_path+'DejaVuSans.ttf', uni=True)
        pdf.add_font('DejaVuBold', '', font_path+'DejaVuSansCondensed-Bold.ttf', uni=True)
        
        for f in fields:
            if f.name in ['id', 'str_hash']  : continue
            pdf.set_font('DejaVuBold', '', 12)
            pdf.write(5, T(f.label))
            pdf.set_font('DejaVu', '', 12)
            pdf.ln(h=5)
            if f.name == 'sex': 
                pdf.write(5, sex_dict[str(item['wkform'][f.name])]) # see db.py for sex_dict
            else:
                pdf.write(5, str(item['wkform'][f.name]))
            pdf.ln(h=8)            
        
        # prepare PDF to download:
        response.headers['Content-Type']='application/pdf'
        return pdf.output(dest='S') 
    return dict(fields=fields, item=item)

def report_all():
    return dict()
    items = db(db.wkform.group_id==db.groups.id).select()
    fields = db.wkform
    
    for item in items:
        item = item.as_dict()
        response.title = item['wkform']['name']+' '+item['wkform']['surname']
        item['wkform']['group_id'] = item['groups']['name']+' ' +item['groups']['weekdays']+' ' +item['groups']['hours']
        
        from gluon.contrib.pyfpdf import FPDF, HTMLMixin
        import os
        font_path = os.getcwd()+'/applications/'+request.application+'/fonts/ttf/'
        file_path = os.getcwd()+'/applications/'+request.application+'/uploads/'
        
        res = []
        
        # create a custom class with the required functionalities 
        class MyFPDF(FPDF, HTMLMixin):
            def header(self): 
                self.add_font('DejaVu', '', font_path+'DejaVuSans.ttf', uni=True)
                self.set_font('DejaVu','',20)
                self.cell(45) # padding
                self.cell(100,10, T('Application Form').strip(),0,0,'C')
                self.ln(10)
                self.cell(155) # padding
                self.cell(30,40, T('photo').strip(),1,0,'C')
                self.ln(10)
                
            def footer(self):
                "hook to draw custom page header"
                self.set_y(-15)
                self.add_font('DejaVu', '', font_path+'DejaVuSans.ttf', uni=True)
                self.set_font('DejaVu','',15)
                #txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
                self.cell(0,10,T('about organization').strip(),0,0,'C')
                #self.write(10, ' '*20+T('about organization'))
                    
        pdf=MyFPDF()
        # create a page and serialize/render HTML objects
        pdf.add_page()
        pdf.add_font('DejaVu', '', font_path+'DejaVuSans.ttf', uni=True)
        pdf.add_font('DejaVuBold', '', font_path+'DejaVuSansCondensed-Bold.ttf', uni=True)
        
        for f in fields:
            if f.name in ['id', 'str_hash']  : continue
            pdf.set_font('DejaVuBold', '', 12)
            pdf.write(5, T(f.label))
            pdf.set_font('DejaVu', '', 12)
            pdf.ln(h=5)
            if f.name == 'sex':
                pdf.write(5, sex_dict[str(item['wkform'][f.name])]) # see db.py for sex_dict
            else:
                pdf.write(5, str(item['wkform'][f.name]))
            pdf.ln(h=8)            
        
        if not os.path.isdir(file_path+item['groups']['name']):
            os.mkdir(file_path+item['groups']['name'])
        pdf.output(file_path+item['groups']['name']+'/'+str(item['wkform']['str_hash'])+'.pdf', 'F')
        res.append(item['wkform']['id'])
    return dict(res=locals())

def send_email():
    return dict()
    import os
    from gluon.tools import Mail
    
    if request.args(0):
        offset = int(request.args(0))
    else:
        offset = 0
    max = offset + 10
    items = db(db.wkform.group_id==db.groups.id).select(limitby=(offset, max))
    res = []
    
    for item in items:
        context = dict(name=str(item['wkform']['name']))
        message = response.render('pupils/message.html', context)
        path_to_pdf = os.getcwd()+'/applications/'+request.application+'/uploads/'+str(item['groups']['name'])+'/'+str(item['wkform']['str_hash'])+'.pdf'
        mail = Mail()
        mail.settings.server = 'smtp.mail.ru'
        mail.settings.login = 'help.won-moscow@mail.ru:annalisa1991'
        mail.settings.sender = 'help.won-moscow@mail.ru'
        res_bool = mail.send(to=[item['wkform']['email']],
            subject='Заполненная анкета из центра Седжон',
            message=message,
            attachments=mail.Attachment(path_to_pdf, content_id='pdf'))
        res.append((item['wkform']['id'], item['wkform']['email'], res_bool))
        response.view = 'pupils/send_email.html'
    return dict(items=res)
