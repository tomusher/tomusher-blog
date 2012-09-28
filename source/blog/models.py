from django.db import models
from misaka import Markdown
from .mdplus import EnhancedRenderer

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
    (3, 'Non-indexed'),
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

    def __unicode__(self):
        return self.name

def markdown_process(text, obj):
    md = Markdown(EnhancedRenderer())
    return md.render(text)

