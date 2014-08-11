# -*- coding: utf-8 -*- line endings: unix -*-
# ------------------------------------------------------------------------------
# miniboa/terminal.py
# Copyright 2009 Jim Storch
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain a
# copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#------------------------------------------------------------------------------
# Changes made by pR0Ps.CM[at]gmail[dot]com on 18/07/2012
# -Updated for use with Python 3.x
# -Repackaged into a single file to simplify distribution
# -Other misc fixes and changes
#
# Report any bugs in this implementation to me (email above)
#------------------------------------------------------------------------------
# Additional changes by Quixadhal on 2014.06.16
# -Re-split code into multiple files, for ease of maintenance
# -Rewrote terminal system
#
# Pinkfish style color codes are now available, as used in various
# LPMUD systems, as well as the I3 intermud network.
#
# Briefly, a color token is surrounded by the special symbol %^, which
# acts as a seperator for multiple tokens in a row.  So, an example like
#
# A %^RED%^red apple%^RESET%^ and a %^BOLD%^BLUE%^blue ball%^RESET%^.
#
# Would result in "red apple" and "blue ball" being colored, and
# "blue ball" would also be in bold.
#
# Some terminals will amke that actual bold, others will make it a
# brighter blue color.
#
# The replacement is dependant on the terminal type passed in, which
# defaults to ANSI, but can be "unknown" to strip colors, or
# "i3" or "imc2" for the intermud networks, or "mxp" for that.
#
# By popular demand, I've also added support for ROM style color codes,
# and also IMC2, and Smaug, since they are parsed in the same way.
#------------------------------------------------------------------------------

"""
Support for color and formatting for various terminals or
terminal-like systems
"""

import logging

logger = logging.getLogger()

import re

from miniboa.colors import TERMINAL_TYPES, COLOR_MAP

_TTYPE_MAP = {
    'tinyfugue': 'ansi',
}

_PARA_BREAK = re.compile(r"(\n\s*\n)", re.MULTILINE)


def word_wrap(text: str, columns=80, indent=4, padding=2):
    """
    Given a block of text, breaks into a list of lines wrapped to
    length.
    """
    paragraphs = _PARA_BREAK.split(text)
    lines = []
    columns -= padding
    for para in paragraphs:
        if para.isspace():
            continue
        line = ' ' * indent
        linelen = len(line)
        words = para.split()
        for word in words:
            bareword = color_convert(word, 'pyom', None)
            if (linelen + 1 + len(bareword)) > columns:
                lines.append(line)
                line = ' ' * padding
                linelen = len(line)
                line += word
                linelen += len(bareword)
            else:
                line += ' ' + word
                linelen += len(bareword) + 1
        if not line.isspace():
            lines.append(line)
    return lines


class Xlator(dict):
    """ All-in-one multiple-string-substitution class """
    def _make_regex(self):
        """ Build re object based on the keys of the current dictionary """
        #x = lambda s: '(?<!' + re.escape(s[0]) + ')' + re.escape(s)
        return re.compile("|".join(map(re.escape, self.keys())))

    def __call__(self, match):
        """ Handler invoked for each regex match """
        return self[match.group(0)][self.otype]

    def xlat(self, text, otype):
        """ Translate text, returns the modified text. """
        self.otype = otype
        return self._make_regex().sub(self, text)


def color_convert(text: str or None, input_type='pyom', output_type='ansi'):
    """
    Given a chunk of text, replace color tokens of the specified input type
    with the appropriate color codes for the given output terminal type
    """
    if not output_type:
        output_type = 'ansi'
    if not input_type:
        input_type = 'rom'
    if text is None or len(text) < 1:
        return text
    if input_type is None or input_type == 'unknown' or input_type not in COLOR_MAP:
        return text
    if output_type is not None and output_type not in TERMINAL_TYPES:
        output_type = None

    if input_type == 'i3':
        words = text.split('%^')
        for word in words:
            if word == '':
                continue
            if word not in COLOR_MAP[input_type]:
                continue
            i = words.index(word)
            if output_type is None:
                words[i] = ''
            else:
                o = TERMINAL_TYPES.index(output_type)
                words[i] = COLOR_MAP[input_type][word][o]
        return ''.join(words)
    else:
        if output_type is None:
            output_type = 'unknown'
        o = TERMINAL_TYPES.index(output_type)
        xl = Xlator(COLOR_MAP[input_type])
        return xl.xlat(text, o)

        # for k in COLOR_MAP[input_type].keys():
        #     if output_type is None:
        #         text = text.replace(k, '')
        #     else:
        #         o = TERMINAL_TYPES.index(output_type)
        #         v = COLOR_MAP[input_type][k][o]
        #         if k != v and v not in COLOR_MAP[input_type]:
        #             text = text.replace(k, v)
        # return text


def escape(text: str, input_type='pyom'):
    """
    Escape all the color tokens in the given text chunk, so they
    can be safely printed through the color parser
    """
    if text is None or text == '':
        return text
    if input_type == 'i3':
        text = text.replace('%^', '%%^^')
    elif input_type == 'pyom':
        text = text.replace('[', '[[')
        text = text.replace(']', ']]')
    elif input_type == 'rom':
        text = text.replace('{', '{{')
        text = text.replace('}', '}}')
    elif input_type == 'smaug':
        text = text.replace('&', '&&')
        text = text.replace('^', '^^')
        text = text.replace('}', '}}')
    elif input_type == 'imc2':
        text = text.replace('~', '~~')
        text = text.replace('^', '^^')
        text = text.replace('`', '``')
    return text


def remap_ttype(ttype: str):
    """
    Remap known terminal types for mud clients and other common terminals
    into one of the supported color mappings, even though we may lose
    information (that we don't use).

    :param ttype:
    :return:
    """
    if ttype in _TTYPE_MAP:
        return _TTYPE_MAP[ttype]
    return ttype
