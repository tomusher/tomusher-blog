from django.db import models
from sorl.thumbnail import get_thumbnail
import markdown

CATEGORIES = (
    ('technology', 'Technology & Video Games'),
    ('boardgames', 'Board Games'),
    ('interesting', 'Interesting'),
    ('dev', 'Development & Design'),
    ('misc', 'Misc'),
)

STATUS = (
    (0, 'Draft'),
    (1, 'Published'),
    (2, 'Idea'),
)

class PostManager(models.Manager):
    def published(self):
        return super(PostManager, self).get_query_set().filter(status=1).order_by('-pub_date')

    def drafts(self):
        return super(PostManager, self).get_query_set().filter(status=0).order_by('-pub_date')

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    link = models.URLField(blank=True)
    pub_date = models.DateTimeField()
    content = models.TextField()
    category = models.CharField(max_length=255, choices=CATEGORIES)
    status = models.IntegerField(choices=STATUS, default=0)

    # Content converted to HTML
    content_html = models.TextField(blank=True)

    # Manager
    objects = PostManager()

    def save(self, *args, **kwargs):
        self.content_html = markdown_process(self.content, self)
        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        y = self.pub_date.strftime("%Y")
        m = self.pub_date.strftime("%m")
        return ('post_detail', [y, m, str(self.slug)])

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-pub_date',)

class Image(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    image = models.ImageField(upload_to="blog-images")

from misaka import Markdown, HtmlRenderer
import re
import shlex
from lxml import etree

class NewRenderer(HtmlRenderer):
    def super_image(self, text):
        alt = text.group(1)
        opts = text.group(9)
        name = ""
        split_opts = [ x.replace("\0", "") for x in shlex.split(opts) ]
        img = etree.Element('img')
        url = split_opts.pop(0)
        img_obj = Image.objects.get(slug=unicode(url)) 
        img.set('alt', alt)
        width, height = (720, 180)
        crop = "center"

        for setting in split_opts:
            if "=" in setting:
                key, val = setting.split("=")
                if key == "size":
                    size = str(val)
                    if "x" in size:
                        size = size.split("x")
                        if size[0]:
                            width = size[0]
                        height = size[1]
                    else:
                        width=size
                elif key == "crop":
                    crop = val
            else:
                name = setting

        img.set('width', str(width))
        img.set('height', str(height))

        thumb = get_thumbnail(img_obj.image, "{0}x{1}".format(width, height), crop=crop)
        img.set('src', thumb.url)
        el = etree.Element('div')
        el.set('class', 'post-image') 
        el.append(img)
        return etree.tostring(el)

    def preprocess(self, text):
        RE =  re.compile(r'\!!' + markdown.inlinepatterns.BRK + r'\s*\((<.*?>|([^\)]*))\)')
        text = RE.sub(self.super_image, text)
                
        return text


def markdown_process(text, obj):
    #md = markdown.Markdown()
    #md.parser.blockprocessors.add('embed_block', EmbedBlockPattern(md.parser), '<paragraph')
    md = Markdown(NewRenderer())
    return md.render(text)

