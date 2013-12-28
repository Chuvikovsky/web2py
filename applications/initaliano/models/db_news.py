# coding: utf8

db.define_table('i_news',
    Field('newstitle','string', length=512, required=True),
    Field('abstract', 'text', length=65536),
    Field('image', 'upload'),
    Field('image_thumb', 'upload', uploadfolder=os.path.join(request.folder,'uploads/thumbs')),
    Field('newstext', 'text', length=65536),
    Field('date_of', 'date'),
    Field('created_at', 'datetime', writable=False, readable=False),
    Field('updated_at', 'datetime', writable=False, readable=False, compute=lambda row: datetime.datetime.now()),
    Field.Virtual('total_price', lambda row: row.image),
)
#db.i_news.thumb = Field.Virtual(lambda row: 'thumbs/'+row.image)

db.i_news.newstitle.requires = IS_NOT_EMPTY()
db.i_news.newstext.requires = IS_NOT_EMPTY()


def create_thumbnail(img, size=(150,150)):
    im_path = os.path.join(request.folder, 'uploads', img)
    if os.path.exists(im_path):
        from PIL import Image
        im = Image.open(im_path)
        im.thumbnail(size, Image.ANTIALIAS)
        thumb_name = img.replace('image', 'image_thumb')
        im.save(os.path.join(request.folder, 'uploads', 'thumbs', thumb_name))
        return thumb_name
    return False

def after_insert_news(news_dict, news_id):
    if news_dict['image']:
        thumb_name = create_thumbnail(news_dict['image'])
        if thumb_name:
            db.i_news[news_id] = dict(image_thumb=thumb_name)

db.i_news._after_insert.append(after_insert_news)
