from django.conf import settings
from mediasync.processors import slim

_settings = {
    'CSS_PATH': "",
    'DOCTYPE': 'html5',
    'EMULATE_COMBO': False,
    'EXPIRATION_DAYS': 365,
    'JOINED': {},
    'JS_PATH': "",
    'STATIC_ROOT': settings.STATIC_ROOT or settings.MEDIA_ROOT,
    'STATIC_URL': settings.STATIC_URL or settings.MEDIA_URL,
    'PROCESSORS': (slim.css_minifier, slim.js_minifier),
    'SERVE_REMOTE': not settings.DEBUG,
    'URL_PROCESSOR': lambda x: x,
}

class Settings(object):
    
    def __init__(self, conf):
        for k, v in conf.iteritems():
            self[k] = v
    
    def __delitem__(self, name):
        del _settings[name]
    
    def __getitem__(self, name):
        return self.get(name)
    
    def __setitem__(self, name, val):
        _settings[name] = val
        
    def __str__(self):
        return repr(_settings)
    
    def get(self, name, default=None):
        return _settings.get(name, default)

msettings = Settings(settings.MEDIASYNC)
