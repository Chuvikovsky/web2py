# -*- coding: utf-8 -*-
# wonkwang form

def onvalidation_f(form):
    str_hash = hash_generator() # see db.py
    form.vars.str_hash = str_hash
    session.str_hash = str_hash
#    path_to_pdf = create_pdf(form)

    from gluon.tools import Mail
    
    email_sent_bool = False
    context = dict(name=str(form.vars['name']))
    message = response.render('form/message.html', context)
    mail = Mail()
    mail.settings.server = 'smtp.mail.ru'
    mail.settings.login = 'help.won-moscow@mail.ru:annalisa1991'
    mail.settings.sender = 'help.won-moscow@mail.ru'
    email_sent_bool = mail.send(to=[form.vars['email']],
        subject='Заполненная анкета из центра Седжон',
        message=message,
        attachments=mail.Attachment(path_to_pdf, content_id='pdf'))
    if email_sent_bool == True:
        session.email_sent = True
    else:
        session.email_sent = False

crud.settings.formstyle = 'ul'
crud.settings.create_next = URL('thanks')
crud.settings.update_next = URL('thanks')
#crud.settings.create_onvalidation = onvalidation_f
#crud.settings.update_onvalidation = onvalidation_f


#db.wkform.assigned_num.requires = [
#        IS_NOT_EMPTY(error_message=T('fill this!')),
#        IS_MATCH('^\d{1,4}$',error_message=T('not a number! Must be a number from 1 to 4 digits'))]

#db.wkform.group_id.requires = IS_IN_SET([(row.id, row.name+' '+row.weekdays+' '+row.hours) for row in db().select(db.groups.ALL, orderby=db.groups.name)])

db.wkform.surname.label = db.wkform.surname.label +  ' *'
db.wkform.surname.comment = "пример: Крузенштерн"
db.wkform.surname.requires = IS_NOT_EMPTY(error_message=T('fill this!'))

db.wkform.name.label = db.wkform.name.label +  ' *'
db.wkform.name.comment = "пример: Иван"
db.wkform.name.requires = IS_NOT_EMPTY(error_message=T('fill this!'))

db.wkform.middlename.label = db.wkform.middlename.label +  ' *'
db.wkform.middlename.comment = "пример: Федорович"
db.wkform.middlename.requires = IS_NOT_EMPTY(error_message=T('fill this!'))

db.wkform.birth_date.label = db.wkform.birth_date.label +  ' *'
db.wkform.birth_date.comment = "пример: 1970-04-25"
db.wkform.birth_date.requires = [
        IS_NOT_EMPTY(error_message=T('fill this!')),
        IS_DATE(format=T('%Y-%m-%d'), error_message=T('must be YYYY-MM-DD!'))]

db.wkform.sex.requires = IS_IN_SET(sex_dict, zero=None)
db.wkform.sex.widget = SQLFORM.widgets.options.widget

#    db.wkform.citizenship

#    db.wkform.passport_number.label = db.wkform.passport_number.label +  ' *'
db.wkform.passport_number.comment = "пример: 4503576342"
#    db.wkform.passport_number.requires = [
#            IS_NOT_EMPTY(error_message=T('fill this!')),
#            IS_MATCH('^\d{10}$',error_message='not a passport number!')]

db.wkform.house_phone.comment = "пример: 4991535452"
#    db.wkform.house_phone.requires = [
#            IS_NOT_EMPTY(error_message=T('fill this!')),
#            IS_MATCH('^\d{10}$',error_message='not a passport number!')]

db.wkform.mobile_phone.label = db.wkform.mobile_phone.label +  ' *'
db.wkform.mobile_phone.comment = "пример: 9035567890"
db.wkform.mobile_phone.requires = [
        IS_NOT_EMPTY(error_message=T('fill this!')),
        IS_MATCH('^\d{10}$',error_message=T('10 digits only!'))]

db.wkform.email.label = db.wkform.email.label +  ' *'
db.wkform.email.comment = "kruzenshtern@yandex.ru"
db.wkform.email.requires = [
        IS_NOT_EMPTY(error_message=T('fill this!')),
        IS_EMAIL(error_message='invalid email!'),
        IS_NOT_IN_DB(db, 'wkform.email')]

db.wkform.address.label = db.wkform.address.label +  ' *'
db.wkform.address.comment = "пример: г. Москва, ул. им. Первой кругосветной экспедиции, 18-21"
db.wkform.address.requires = [IS_NOT_EMPTY(error_message=T('fill this!'))]
db.wkform.address.widget = SQLFORM.widgets.text.widget

db.wkform.academic.label = db.wkform.academic.label +  ' *'
db.wkform.academic.comment = "пример: ООО 'Русско-американская компания'"
db.wkform.academic.requires = [IS_NOT_EMPTY(error_message=T('fill this!'))]
db.wkform.academic.widget = SQLFORM.widgets.text.widget

db.wkform.speciality.label = db.wkform.speciality.label +  ' *'
db.wkform.speciality.comment = "пример: начальник кругосветной экспедиции"
db.wkform.speciality.requires = [IS_NOT_EMPTY(error_message=T('fill this!'))]
db.wkform.speciality.widget = SQLFORM.widgets.text.widget

db.wkform.why_korean.label = db.wkform.why_korean.label +  ' *'
db.wkform.why_korean.requires = [IS_NOT_EMPTY(error_message=T('fill this!'))]

def thanks():
    txt = '''Спасибо, Ваша анкета принята.
        На email, указанный Вами в анкете отправлена заполненная анкета.'''
    return dict(txt=txt)

def index():
    email_form = SQLFORM.factory(Field('email', requires=[IS_NOT_EMPTY(),IS_EMAIL()]))
    if email_form.process().accepted:
        record = db(db.wkform.email==email_form.vars.email).select().first()
        session.email = email_form.vars.email
        if record:
            txt = '''Указанный Вами email уже есть в нашей базе данных.
                    Это означает, что ранее Вы уже заполняли анкету на сайте.
                    На Ваш email будет выслано письмо для подтверждения, что Вы являетесь
                    владельцем этого электронного адреса. Перейдите по ссылке, указанной в письме,
                     на страницу с информацией, которую Вы вносили раньше.
                '''
            response.view = 'form/confirmation.html'
            session.record_id = record.id
            return dict(txt=txt)
        else:
            txt = '''Указанного Вами email нет в нашей базе данных. Вам придется заполнить анкету-заявление.
            '''
    return dict(form=email_form)

def confirmation():
    if not session.email and not session.record_id:
        redirect(URL('index'))
    record = db.wkform(session.record_id)
    import hashlib, datetime
    email_hash = hashlib.md5(str(datetime.datetime.now())+record.email).hexdigest()
    record.update_record(email_hash=email_hash)
    if record.completed == 'None':
        record.update_record(completed=datetime.datetime.now())
    url = URL('wkform', args=[email_hash], scheme=True, host=True)

    from gluon.tools import Mail
    message = response.render('form/conf_message.html', dict(name=str(record.name), url=url))
    mail = Mail()
    mail.settings.server = 'smtp.mail.ru'
    mail.settings.login = 'help.won-moscow@mail.ru:annalisa1991'
    mail.settings.sender = 'help.won-moscow@mail.ru'
    email_sent_bool = mail.send(to=['chuvikovsky@yandex.ru'],
        subject='Подтверждение email. Центр Седжон',
        message=message)
    if email_sent_bool == True:
        session.email_sent = True
    else:
        session.email_sent = False

def wkform():
    if not request.args(0):
        form = crud.create(db.wkform)
    record = db(db.wkform.email_hash==request.args(0)).select().first()
    if record:
        form = crud.update(db.wkform, record)
    else:
        form = crud.create(db.wkform)
    return dict(form=form)

def hidden_update():
    response.view = 'form/hidden.html'
    form = crud.update(db.wkform, request.args(0))
    return dict(form=form)
        
def hidden():

    
    form = crud.create(db.wkform)
                                                                                                                                                                
    return dict(form=form)

def create_pdf(form):
    group = db(db.groups.id==form.vars.group_id).select().first().as_dict()
    fields = db.wkform
    group_str = group['name']+' ' +group['weekdays']+' ' +group['hours']

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
        if f.name in ['id', 'completed', 'str_hash']: continue
        pdf.set_font('DejaVuBold', '', 12)
        pdf.write(5, T(f.name))
        pdf.set_font('DejaVu', '', 12)
        pdf.ln(h=5)
        if f.name == 'sex': 
            pdf.write(5, sex_dict[str(form.vars[f.name])]) # see db.py for sex_dict
        elif f.name == 'group_id':
            pdf.write(5, group_str)
        elif form.vars[f.name] == None:
            pdf.write(5, ' ')
        else:
            pdf.write(5, str(form.vars[f.name]))
        pdf.ln(h=8)            
    
    if not os.path.isdir(file_path+group['name']):
        os.mkdir(file_path+group['name'])
    path_to_pdf = file_path+group['name']+'/'+str(form.vars['str_hash'])+'.pdf'
    pdf.output(path_to_pdf, 'F')
    return path_to_pdf

def report():
    item = db((db.wkform.group_id==db.groups.id) & (db.wkform.str_hash==request.args(0))).select().first().as_dict()
    response.title = item['wkform']['name']+' '+item['wkform']['surname']
    fields = db.wkform
    item['wkform']['group_id'] = item['groups']['name']+' ' +item['groups']['weekdays']+' ' +item['groups']['hours']

    if request.extension=="pdf":
        from gluon.contrib.pyfpdf import FPDF, HTMLMixin
        import os
        font_path = os.getcwd()+'/applications/'+request.application+'/fonts/ttf/'
        
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

def f():
    rows = db(db.wkform.completed==None).select()
    return {'rows': rows}
