from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from mediasync import MEDIA_URL
import warnings

JOINED = getattr(settings, "MEDIASYNC_JOINED", {})
SERVE_REMOTE = getattr(settings, "MEDIASYNC_SERVE_REMOTE", not settings.DEBUG)
DOCTYPE = getattr(settings, "MEDIASYNC_DOCTYPE", 'xhtml')

register = template.Library()

#
# media stuff
#

@register.simple_tag
def media_url():
    return MEDIA_URL

#
# CSS related tags
#

LINK_ENDER = ' />' if DOCTYPE == 'xhtml' else '>'

def linktag(url, path, filename, media):
    if path:
        url = "%s/%s" % (url, path)
    params = (url, filename, media, LINK_ENDER)
    return """<link rel="stylesheet" href="%s/%s" type="text/css" media="%s"%s""" % params
    
@register.simple_tag
def css(filename, media="screen, projection"):
    css_path = getattr(settings, "MEDIASYNC_CSS_PATH", "").strip('/')
    if SERVE_REMOTE and filename in JOINED:
        return linktag(MEDIA_URL, css_path, filename, media)
    else:
        filenames = JOINED.get(filename, (filename,))
        return ' '.join((linktag(MEDIA_URL, css_path, fn, media) for fn in filenames))

@register.simple_tag
def css_print(filename):
    return css(filename, media="print")

@register.simple_tag
def css_ie(filename):
    warnings.warn("mediasync css_ie template tag has been deprecated", DeprecationWarning)
    return """<!--[if IE]>%s<![endif]-->""" % css(filename)

@register.simple_tag
def css_ie6(filename):
    warnings.warn("mediasync css_ie6 template tag has been deprecated", DeprecationWarning)
    return """<!--[if IE 6]>%s<![endif]-->""" % css(filename)

@register.simple_tag
def css_ie7(filename):
    warnings.warn("mediasync css_ie7 template tag has been deprecated", DeprecationWarning)
    return """<!--[if IE 7]>%s<![endif]-->""" % css(filename)

#
# JavaScript related tags
#

def scripttag(url, path, filename):
    if path:
        url = "%s/%s" % (url, path)
    if DOCTYPE == 'html5':
        markup = """<script src="%s/%s"></script>"""
    else:
        markup = """<script type="text/javascript" charset="utf-8" src="%s%s/%s"></script>"""
    return markup % (url, filename)
    
@register.simple_tag
def js(filename):
    js_path = getattr(settings, "MEDIASYNC_JS_PATH", "").strip('/')
    if SERVE_REMOTE and filename in JOINED:
        return scripttag(MEDIA_URL, js_path, filename)
    else:
        filenames = JOINED.get(filename, (filename,))
        return ' '.join((scripttag(MEDIA_URL, js_path, fn) for fn in filenames))

#
# conditional tags
#

@register.tag
def ie(parser, token):
    condition_format = """<!--[if IE]>%s<![endif]-->"""
    return conditional(parser, token, condition_format, "endie")
    
@register.tag
def ie6(parser, token):
    condition_format = """<!--[if IE 6]>%s<![endif]-->"""
    return conditional(parser, token, condition_format, "endie6")
    
@register.tag
def ie7(parser, token):
    condition_format = """<!--[if IE 7]>%s<![endif]-->"""
    return conditional(parser, token, condition_format, "endie7")

def conditional(parser, token, condition_format, endtag):
    contents = token.split_contents()
    warnings.warn("mediasync %s template tag has been deprecated" % contents[0], DeprecationWarning)
    newline = 'newline' in contents
    nodelist = parser.parse((endtag,))
    parser.delete_first_token()
    return ConditionalNode(nodelist, condition_format, newline)

class ConditionalNode(template.Node):
    
    def __init__(self, nodelist, condition_format, newline=False):
        self.nodelist = nodelist
        self.condition_format = condition_format
        self.newline = newline

    def render(self, context):
        inner = self.nodelist.render(context)
        if self.newline:
            inner = "\n%s\n" % inner
        return self.condition_format % inner