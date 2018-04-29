import sys

__all__ = ['BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE',
           'format',
           'hline']

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = list(range(8))

TERMINAL_WIDTH = 80

hline = '-' * TERMINAL_WIDTH


# following from Python cookbook, #475186
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False  # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False


has_colours = has_colours(sys.stdout)


def format(text, color=None, align='l'):
    if color:
        text = _set_color(text, color)

    text = _set_alignment(text, align)

    return text


################################################
# Private functions called by format function. #
################################################


def _set_color(text, colour):
    if has_colours:
        seq = "\x1b[1;{color}m".format(color=30 + colour) + text + "\x1b[0m"
        return seq
    else:
        return text


def _set_alignment(text, mode):
    if mode == 'c':
        translated_mode = '^'
    elif mode == 'r':
        translated_mode = '>'
    else:
        translated_mode = '<'
    return '{:{align}{width}}'.format(text, align=translated_mode, width=TERMINAL_WIDTH)
