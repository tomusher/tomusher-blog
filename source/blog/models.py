from django.db import models
import markdown

CATEGORIES = (
    ('technology', 'Technology & Video Games'),
    ('boardgames', 'Board Games'),
    ('interesting', 'Interesting'),
    ('dev', 'Development & Design'),
    ('misc', 'Misc'),
)

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    link = models.URLField(blank=True)
    published_date = models.DateTimeField()
    content = models.TextField()
    category = models.CharField(max_length=255, choices=CATEGORIES)

    # Content converted to HTML
    content_html = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.content_html = markdown_process(self.content, self)
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

class Image(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    image = models.ImageField(upload_to="blog-images")

def markdown_process(text, obj):
    md = markdown.Markdown()
    #md.treeprocessors['populateimage'] = PopulateImageReferences(md)
    #md.extensions = ['extra']
    return md.convert(text)

#class PopulateImageReferences(markdown.treeprocessors.Treeprocessor):
#    def run(self, root):
#        images = root.getiterator('img')
#
#        for img in images:
#            slug = img.attrib.get('alt')
#            imgObj = Image.objects.get(slug=slug) 
#            thumb = get_thumbnail(imgObj.image, "960x320", crop="center")
#            img.set('src', thumb.url)

        

