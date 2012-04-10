from django.db import models
import markdown
from embedly import Embedly
from markdown import etree
from sorl.thumbnail import get_thumbnail
import re

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
)

class PostManager(models.Manager):
    def published(self):
        return super(PostManager, self).get_query_set().filter(status=1).order_by('-pub_date')

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    link = models.URLField(blank=True)
    pub_date = models.DateTimeField()
    content = models.TextField()
    category = models.CharField(max_length=255, choices=CATEGORIES)
    status = models.IntegerField(choices=STATUS)

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

class Image(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    image = models.ImageField(upload_to="blog-images")

def markdown_process(text, obj):
    md = markdown.Markdown()
    md.parser.blockprocessors.add('embed_block', EmbedBlockPattern(md.parser), '<paragraph')
    return md.convert(text)

class EmbedBlockPattern(markdown.blockprocessors.BlockProcessor):
    RE =  re.compile(r'\!!' + markdown.inlinepatterns.BRK + r'\s*\((<.*?>|([^\)]*))\)')

    def test(self, parent, block):
        return bool(self.RE.search(block))
    
    def run(self, parent, blocks):
        block = blocks.pop(0)
        for i in self.RE.finditer(block):
            match = self.RE.match(block)
            src_parts = match.group(9).split()
            url = src_parts[0]
            self.size = ""
            if len(src_parts) > 1:
                self.size = src_parts[1]
            if url.startswith('http://'):
                el = self.embed(url)
            else:
                el = self.image(url)

            parent.append(el)

    def embed(self, url):
        embed = Embedly('799502ba808f11e18d6f4040d3dc5c07')
        if not self.size:
            self.size = "640x480"

        try:
            width, height = self.size.split('x')
            opts = {'width': width, 'height':height}
        except:
            opts = {}

        obj = embed.oembed(url, **opts)
        el = etree.Element('div')
        el.text = obj.html
        return el
    
    def image(self, url):
        if not self.size:
            self.size = "780x260"

        img = etree.Element('img')
        img_obj = Image.objects.get(slug=url) 
        thumb = get_thumbnail(img_obj.image, self.size, crop="center")
        img.set('src', thumb.url)
        el = etree.Element('div')
        el.append(img)
        el.set('class', 'post-image') 
        return el
