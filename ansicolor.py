# Author: Martin Matusiak <numerodix@gmail.com>
# Licensed under the GNU Public License, version 3.
#
# url: http://github.com/numerodix/pybits


__all__ = ['Colors', 'colorize', 'get_code', 'get_highlighter',
           'strip_escapes', 'wrap_string', 'write_out', 'write_err']


import os

_disable = (not os.environ.get("TERM")) or (os.environ.get("TERM") == "dumb")


class Colors(object):
    @classmethod
    def new(cls, colorname):
        try:
            _ = cls.colorlist
        except AttributeError:
            cls.colorlist = []

        newcls = type.__new__(type, colorname, (object,), {})
        newcls.id = len(cls.colorlist)

        cls.colorlist.append(newcls)
        setattr(cls, colorname, newcls)

    @classmethod
    def iter(cls):
        for color in cls.colorlist:
            yield color

Colors.new("Black")
Colors.new("Red")
Colors.new("Green")
Colors.new("Yellow")
Colors.new("Blue")
Colors.new("Magenta")
Colors.new("Cyan")
Colors.new("White")


_highlights = [
    Colors.Green,
    Colors.Yellow,
    Colors.Cyan,
    Colors.Blue,
    Colors.Magenta,
    Colors.Red
]

_highlight_map = {}
for (n, h) in enumerate(_highlights):
    _highlight_map[n] = [color for color in Colors.iter() if h == color].pop()

def get_highlighter(colorid):
    '''Map a color index to a highlighting color'''
    return _highlight_map[colorid % len(_highlights)]

def get_code(color, bold=False, reverse=False):
    '''Return escape code for styling with color, bold or reverse'''
    if _disable:
        return ""

    bold = (bold == True) and 1 or 0
    if reverse:
        return "\033[7m"
    if not color:
        return "\033[0m"
    return "\033[%s;3%sm" % (bold, color.id)

def colorize(s, color, bold=False, reverse=False):
    '''Colorize the string'''
    return "%s%s%s" % (get_code(color, bold=bold, reverse=reverse), s, get_code(None))

def wrap_string(s, pos, color, bold=False, reverse=False):
    '''Colorize the string up to a position'''
    if _disable:
        if pos == 0: pos = 1
        return s[:pos-1] + "|" + s[pos:]

    return "%s%s%s%s" % (get_code(color, bold=bold, reverse=reverse),
                         s[:pos],
                         get_code(None),
                         s[pos:])

def strip_escapes(s):
    '''Strip escapes from string'''
    import re
    return re.sub('\033[[](?:(?:[0-9]*;)*)(?:[0-9]*m)', '', s)

def write_to(target, s):
    # assuming we have escapes in the string
    if not _disable:
        if not os.isatty(target.fileno()):
            s = strip_escapes(s)
    target.write(s)
    target.flush()

def write_out(s):
    '''Write a string to stdout, strip escapes if output is a pipe'''
    write_to(sys.stdout, s)

def write_err(s):
    '''Write a string to stderr, strip escapes if output is a pipe'''
    write_to(sys.stderr, s)


if __name__ == '__main__':
    import sys
    lst = []
    for color in Colors.iter():
        line = []
        line.append( colorize(color.__name__, color) )
        line.append( colorize(color.__name__, color, bold=True) )
        line.append( colorize(color.__name__, color, reverse=True) )
        line.append( colorize(color.__name__, color, bold=True, reverse=True) )
        lst.append(line)

    for line in lst:
        for item in line:
            w = len(item) + (10 - len(strip_escapes(item)))
            sys.stdout.write("%s" % item.ljust(w))
        sys.stdout.write("\n")
