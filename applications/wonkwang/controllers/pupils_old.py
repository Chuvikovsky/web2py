# -*- coding: utf-8 -*-

# admin module for wonkwang.ru form

def links_opt(row):
    if request.args(0):
        return  A('pdf', _href=URL('report.pdf', args=row.id))
    else:
        return  A('pdf', _href=URL('report.pdf', args=row.wkform.id))

def index():
    grid = SQLFORM.grid(db.wkform,
        fields=[db.wkform.id, db.wkform.str_hash, db.wkform.surname, db.wkform.name, db.wkform.str_hash,
                    db.wkform.middlename, db.wkform.email, db.groups.name, 
                    db.groups.weekdays, db.groups.hours, db.wkform.completed],
        left=db.wkform.on(db.groups.id==db.wkform.group_id),
        links=[dict(header='Pdf', body=links_opt)])
    return dict(grid=grid)

def report():
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
	import os
	items = db(db.wkform.group_id==db.groups.id).select()
	for item in items:
		if item['wkform']['id'] != 87:
			continue
		from gluon.tools import Mail
		mail = Mail()
		mail.settings.server = 'smtp.mail.ru'
		mail.settings.login = 'help.won-moscow@mail.ru:annalisa1991'
		mail.settings.sender = 'help.won-moscow@mail.ru'
		message = 'Уважаемый(ая) '+str(item['wkform']['name'])
		message += '''
	
		придумайте, пожалуйста, текст письма, 
		а также напишите подробнее, что же побудило Вас изучать корейский язык
		'''
		res = mail.send(to=['chuvikovsky@gmail.com', item['wkform']['email']],
			subject='Заполненная анкета из центра Седжон',
			message=message,
			attachments=mail.Attachment(
				os.getcwd()+'/applications/'+request.application
				+'/uploads/'+str(item['groups']['name'])
				+'/'+str(item['wkform']['str_hash'])+'.pdf', 
				content_id='pdf'))
	return dict(items=locals())
