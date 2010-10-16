import re

class Language(object):
    def __init__(self, name, extensions, comment_filters, filename_patterns=tuple()):
        self.name = name
        self.extensions = extensions
        self.comment_filters = {'to_eol': ([re.compile(p) for p in comment_filters['to_eol']]
                                           if 'to_eol' in comment_filters else tuple()),
                                'between': (comment_filters['between']
                                            if 'between' in comment_filters else tuple())}
        self.filename_patterns = [re.compile(p) for p in filename_patterns]

    @staticmethod
    def by_name(name):
        for l in LANGUAGES:
            if l.name == name:
                return l
        return None

    @staticmethod
    def from_filename(filename):
        for l in LANGUAGES:
            if (any(filename.endswith('.%s' % (ext, )) for ext in l.extensions) or
                any(re.match(pattern, filename) for pattern in l.filename_patterns)):
                return l
        return None


C_STYLE_COMMENTS = {'to_eol': ('//', ),
                    'between': (('/\*', '\*/'), )}

LANGUAGES = (Language('C/C++',
                      ('c', 'c++', 'cc', 'cpp'),
                      C_STYLE_COMMENTS),
             Language('C/C++ Header',
                      ('h', 'h++', 'hh', 'hpp'),
                      C_STYLE_COMMENTS),
             Language('C#',
                      ('cs', ),
                      C_STYLE_COMMENTS),
             Language('Python',
                      ('py', ),
                      {'to_eol': ('#', )}),
             Language('Makefile',
                      tuple(),
                      {'to_eol': ('#', )},
                      filename_patterns=('^(GNU)?Makefile.*', )),
             Language('XAML',
                      ('xaml', ),
                      {'between': (('<!--', '-->'), )}),
             )
