import re
import shlex
import models
from lxml import etree, html
from misaka import HtmlRenderer
from sorl.thumbnail import get_thumbnail
from embedly import Embedly
from django.conf import settings

class EnhancedRenderer(HtmlRenderer):
    def enhanced_image(self, text):
        overwritten_options = self.parse_options(text)  
        
        options = {
            "width": "720",
            "height": "180",
            "crop": "center",
            "extra_class": "",
        }

        options.update(overwritten_options)
        
        return self.create_image(options)

    def enhanced_embed(self, text):
        overwritten_options = self.parse_options(text)  
        
        options = {
            "width": "560",
            "height": "315",
            "extra_class": "",
        }

        options.update(overwritten_options)
        
        return self.create_embed(options)

    def create_embed(self, options):
        embed = Embedly(settings.EMBEDLY_API_KEY)

        obj = embed.oembed(options['url'], width=options['width'], height=options['height'])
        el = etree.Element('div')
        el.set('class', 'post-embed')
        el.append(html.fromstring(obj.html))
        return etree.tostring(el)

    def create_image(self, options):
        attr_map = {
            "alt": "alt_text",
            "width": "width",
            "height": "height",
        }
        img = etree.Element('img')
        img_obj = models.Image.objects.get(
                slug=unicode(options['url'])) 

        thumb = get_thumbnail(
                img_obj.image, 
                "{0}x{1}".format(options['width'], options['height']), 
                crop=options['crop'])

        larger = get_thumbnail(
                img_obj.image,
                options['width'],
                crop="center")

        for attr, src in attr_map.iteritems():
            img.set(attr, options[src])

        img.set('src', thumb.url)

        el = etree.Element('a')
        el.set('class', 
                'post-image {0}'.format(
                    options['extra_class'])
                ) 
        el.set('href', larger.url)
        el.append(img)
        return etree.tostring(el)

    def parse_size_string(self, size):
        if 'x' in size:
            size = size.split("x")
            if size[0]:
                width = size[0]
            height = size[1]
        else:
            width = size
        return (width, height)

    def parse_options(self, text):
        options = {}
        options['alt_text'] = text.group(1)
        remaining_options = text.group(9)
        split_options = [ x.replace("\0", "") for x in shlex.split(remaining_options) ]
        
        options['url'] = split_options.pop(0)

        for option in split_options:
            key, val = option.split("=")
            options[key] = val

        if 'size' in options:
            width, height = self.parse_size_string(options['size'])
            options['width'] = width
            options['height'] = height

        return options

    def preprocess(self, text):
        img_tag_re = r'\[([^\]\[]*(\[[^\]\[]*(\[[^\]\[]*(\[[^\]\[]*(\[[^\]\[]*(\[[^\]\[]*(\[[^\]\[]*\])*[^\]\[]*\])*[^\]\[]*\])*[^\]\[]*\])*[^\]\[]*\])*[^\]\[]*\])*[^\]\[]*)\]\s*\((<.*?>|([^\)]*))\)'
        image_re =  re.compile(r'\!!' + img_tag_re)
        embed_re =  re.compile(r'\@' + img_tag_re)
        text = image_re.sub(self.enhanced_image, text)
        text = embed_re.sub(self.enhanced_embed, text)
                
        return text
    
