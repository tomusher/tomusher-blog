from django import template
from django.core.urlresolvers import reverse, resolve
from blog.models import Image
import re
from pygments import lexers, highlight
from pygments.formatters import HtmlFormatter

register = template.Library()

@register.inclusion_tag('image.html')
def image(slug):
    image = Image.objects.get(slug=slug)
    print image.image.url
    return {'image': image}

@register.tag
def code(parser, token):
    try:
        tag_name, language = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    language = language[1:-1]
    nodelist = parser.parse(('endcode',))
    parser.delete_first_token()
    return CodeNode(nodelist, language)

class CodeNode(template.Node):
    def __init__(self, nodelist, language):
        self.nodelist = nodelist
        self.language = language

    def render(self, context):
        output = self.nodelist.render(context)
        return self.highlight(output)

    def highlight(self, code):
        code_re = re.compile(r'<code(.*?)>(.*?)</code>', re.DOTALL) 
        pre_re = re.compile(r'<pre>(.*?)</pre>', re.DOTALL) 

        lexer = lexers.get_lexer_by_name(self.language)
        pygmentized_code = highlight(code, lexer, CodeHtmlFormatter())
        
        return pygmentized_code


class CodeHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_code(source)
    
    def _wrap_code(self, source):
        yield 0, '<div class="highlight"><pre><code>'
        for i, t in source:
            yield i, t
        yield 0, '</code></pre></div>'
