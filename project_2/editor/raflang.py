import re
from pygments.lexer import RegexLexer
from pygments.token import Text, Punctuation, Number, Operator, Keyword

__all__ = ['RafLangLexer']

class RafLangLexer(RegexLexer):
    name = 'raflang'
    aliases = ['raflang', 'raf']
    filenames = ['*.raf']
    
    tokens = {
        'root': [
            (r'\s+', Text),
            (r'(\:|\|)', Punctuation),
            (r'\d+[eE][+-]?[0-9]+j?', Number.Float),
            (r'\d+j?', Number.Integer),
            (r'!=|==|<<|>>|[-+/*%=<>]', Operator),
            (r'##?('
                'program'
                '|postojanje'
                '|dodela'
                '|celina'
                '|naredba'
                '|rutina'
                '|~rutina'
                '|~ugradjena_rutina'
                '|vrati'
                '|polje'
                ')', Keyword)
        ]
    }
