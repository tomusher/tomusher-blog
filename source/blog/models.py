from django.db import models
import markdown
from embedly import Embedly
from markdown import etree
from sorl.thumbnail import get_thumbnail


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
    EMBED_LINK_RE = r'\!!' + markdown.inlinepatterns.BRK + r'\s*\((<.*?>|([^\)]*))\)'
    embed_tag = EmbedLinkPattern(EMBED_LINK_RE, md)
    md.inlinePatterns.add('embed_link', embed_tag, '<image_link')
    md.inlinePatterns['image_link'] = ImageLinkPattern(markdown.inlinepatterns.IMAGE_LINK_RE, md)
    #md.treeprocessors['populateimage'] = PopulateImageReferences(md)
    md.extensions = ['extra']
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

class ImageLinkPattern(markdown.inlinepatterns.ImagePattern):
    def handleMatch(self, m):
        imgpattern = markdown.inlinepatterns.ImagePattern(self.pattern, self.markdown)
        el = imgpattern.handleMatch(m)
        slug = el.get('src')
        if not slug.startswith('http://'):
            imgObj = Image.objects.get(slug=slug) 
            thumb = get_thumbnail(imgObj.image, "960x320", crop="center")
            el.set('src', thumb.url)
        return el

class EmbedLinkPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        embed = Embedly('799502ba808f11e18d6f4040d3dc5c07')
        src_parts = m.group(9).split()
        obj = embed.oembed(src_parts[0])
        el = etree.Element('div')
        el.text = obj.html
        return el

