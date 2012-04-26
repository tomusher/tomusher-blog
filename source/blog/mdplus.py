import markdown
from markdown import etree
from sorl.thumbnail import get_thumbnail
import re
from embedly import Embedly
import models
from django.conf import settings

class EmbedBlockPattern(markdown.blockprocessors.BlockProcessor):
    RE =  re.compile(r'\!!' + markdown.inlinepatterns.BRK + r'\s*\((<.*?>|([^\)]*))\)')

    def test(self, parent, block):
        return bool(self.RE.search(block))
    
    def run(self, parent, blocks):
        block = blocks.pop(0)
        for i in self.RE.finditer(block):
            match = self.RE.match(block)
            alt = match.group(1)
            src_parts = match.group(9).split()
            url = src_parts[0]
            self.size = ""
            if len(src_parts) > 1:
                self.size = src_parts[1]
            if url.startswith('http://'):
                el = self.embed(url)
            else:
                el = self.image(url, alt)

            parent.append(el)

    def embed(self, url):
        embed = Embedly(settings.EMBEDLY_API_KEY)
        if not self.size:
            self.size = "560x315"

        try:
            width, height = self.size.split('x')
            opts = {'width': width, 'height':height}
        except:
            opts = {}

        obj = embed.oembed(url, **opts)
        el = etree.Element('div')
        el.set('class', 'post-embed')
        el.text = obj.html
        return el
    
    def image(self, url, alt):
        if not self.size:
            self.size = "780x260"

        img = etree.Element('img')
        img_obj = models.Image.objects.get(slug=url) 
        thumb = get_thumbnail(img_obj.image, self.size, crop="center")
        width, height = self.size.split('x')
        img.set('width', width)
        img.set('height', height)
        img.set('src', thumb.url)
        img.set('alt', alt)
        el = etree.Element('div')
        el.append(img)
        el.set('class', 'post-image') 
        return el
