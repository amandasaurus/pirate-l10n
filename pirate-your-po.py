#! /usr/bin/env python

__author__ = 'Rory McCann <rory@technomancy.org>'
__version__ = '1.0'
__licence__ = 'GPLv3'

import polib, subprocess, re, sys

def translate_subpart(string):
    """Converts the whole of the string to pirate speak by (a) passing it through our custom replacements and (b) passing it through pirate on the command line"""
    replacements = [
        # ('boring english version', 'exciting pirate version'),
        # Add extra translations here
        ('Log in', 'Set sail'), ('login', 'set sail'), ('log in', 'set sail'), ('Login', 'Set sail'),
        ('Log out', 'Abandon Ship'), ('logout', 'abandon ship'), ('log out', 'abandon ship'), ('Logout', 'Abandon Ship'),
        ('password', 'secret code'), ('Password', 'Secret Code'),
    ]
    for old, new in replacements:
        string = string.replace(old, new)

    translater = subprocess.Popen('pirate', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    translater.stdin.write(string.encode("utf8")+"\n")
    output, _ = translater.communicate()
    output = output[:-1]
    return output.decode("utf8")

def translate(string):
    """Takes a string that is to be translated and returns the translated string, doesn't translate the %(format)s parts, they must remain the same text as the msgid"""
    output = ""
    for index, part in enumerate(re.split(r"(%\([^\)]+\)?.|\%[^\(])", string)):
        if index % 2 == 0:
            # This is not a format specifier
            output += translate_subpart(part)
        else:
            output += part

    return output


def piratize_po(filename):
    """Given a .po file, converts the text to pirate speak then saves it"""
    pofile = polib.pofile(filename)
    for entry in pofile:
        entry.msgstr = translate(entry.msgid)

    pofile.save(filename)

if __name__ == '__main__':
    piratize_po(sys.argv[1])
