# -*- coding: utf-8 -*- line endings: unix -*-
# ------------------------------------------------------------------------------
# miniboa/colors.py
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
# acts as a separator for multiple tokens in a row.  So, an example like
#
# A %^RED%^red apple%^RESET%^ and a %^BOLD%^BLUE%^blue ball%^RESET%^.
#
# Would result in "red apple" and "blue ball" being colored, and
# "blue ball" would also be in bold.
#
# Some terminals will make that actual bold, others will make it a
# brighter blue color.
#
# The replacement is dependant on the terminal type passed in, which
# defaults to ANSI, but can be "unknown" to strip colors, or
# "i3" or "imc2" for the intermud networks, or "mxp" for that.
#------------------------------------------------------------------------------
"""
Split off the color codes themselves into a separate module
to make it easier to edit the actual terminal code
"""

import logging

logger = logging.getLogger()

from collections import namedtuple

TERMINAL_TYPES = ('unknown', 'pyom', 'rom', 'smaug', 'imc2', 'ansi', 'greyscale', 'i3', 'mxp')

ColorToken = namedtuple('ColorToken', TERMINAL_TYPES)

COLOR_MAP = {}

COLOR_MAP['unknown'] = {
}

COLOR_MAP['pyom'] = {
    '[d': ColorToken('',    '[d',   '{d',   '&x',   '~x',   '\033[30m',     '\033[38;5;232m',   '%^BLACK%^',            '<COLOR FORE=\"#000000\">' ),
    '[r': ColorToken('',    '[r',   '{r',   '&r',   '~r',   '\033[31m',     '\033[38;5;237m',   '%^RED%^',              '<COLOR FORE=\"#bb0000\">' ),
    '[g': ColorToken('',    '[g',   '{g',   '&g',   '~g',   '\033[32m',     '\033[38;5;237m',   '%^GREEN%^',            '<COLOR FORE=\"#00bb00\">' ),
    '[y': ColorToken('',    '[y',   '{y',   '&O',   '~y',   '\033[33m',     '\033[38;5;244m',   '%^ORANGE%^',           '<COLOR FORE=\"#bbbb00\">' ),
    '[b': ColorToken('',    '[b',   '{b',   '&b',   '~b',   '\033[34m',     '\033[38;5;237m',   '%^BLUE%^',             '<COLOR FORE=\"#0000bb\">' ),
    '[m': ColorToken('',    '[m',   '{m',   '&p',   '~p',   '\033[35m',     '\033[38;5;244m',   '%^MAGENTA%^',          '<COLOR FORE=\"#bb00bb\">' ),
    '[c': ColorToken('',    '[c',   '{c',   '&c',   '~c',   '\033[36m',     '\033[38;5;244m',   '%^CYAN%^',             '<COLOR FORE=\"#00bbbb\">' ),
    '[w': ColorToken('',    '[w',   '{w',   '&w',   '~w',   '\033[37m',     '\033[38;5;250m',   '%^WHITE%^',            '<COLOR FORE=\"#bbbbbb\">' ),

    '[D': ColorToken('',    '[D',   '{D',   '&z',   '~z',   '\033[1;30m',   '\033[38;5;240m',   '%^BOLD%^BLACK%^',      '<COLOR FORE=\"#555555\">'),
    '[R': ColorToken('',    '[R',   '{R',   '&R',   '~R',   '\033[1;31m',   '\033[38;5;245m',   '%^BOLD%^RED%^',        '<COLOR FORE=\"#ff5555\">'),
    '[G': ColorToken('',    '[G',   '{G',   '&G',   '~G',   '\033[1;32m',   '\033[38;5;245m',   '%^BOLD%^GREEN%^',      '<COLOR FORE=\"#55ff55\">'),
    '[Y': ColorToken('',    '[Y',   '{Y',   '&Y',   '~Y',   '\033[1;33m',   '\033[38;5;251m',   '%^BOLD%^ORANGE%^',     '<COLOR FORE=\"#ffff55\">'),
    '[B': ColorToken('',    '[B',   '{B',   '&B',   '~B',   '\033[1;34m',   '\033[38;5;245m',   '%^BOLD%^BLUE%^',       '<COLOR FORE=\"#5555ff\">'),
    '[M': ColorToken('',    '[M',   '{M',   '&P',   '~P',   '\033[1;35m',   '\033[38;5;251m',   '%^BOLD%^MAGENTA%^',    '<COLOR FORE=\"#ff55ff\">'),
    '[C': ColorToken('',    '[C',   '{C',   '&C',   '~C',   '\033[1;36m',   '\033[38;5;251m',   '%^BOLD%^CYAN%^',       '<COLOR FORE=\"#55ffff\">'),
    '[W': ColorToken('',    '[W',   '{W',   '&W',   '~W',   '\033[1;37m',   '\033[38;5;255m',   '%^BOLD%^WHITE%^',      '<COLOR FORE=\"#ffffff\">'),

    '[*': ColorToken('',    '[*',   '{*',   '',     '',     '\007',         '\007',             '',                     ''),
    '[/': ColorToken('',    '[/',   '{/',   '',     '',     '\012',         '\012',             '',                     ''),

    '[[': ColorToken('[',   '[[',   '[',    '[',    '[',    '[',            '[',                '[',                    '['),
    ']]': ColorToken(']',   ']]',   ']',    ']',    ']',    ']',            ']',                ']',                    ']'),

    '[x': ColorToken('',    '[x',   '{x',   '&d',   '~!',   '\033[0m',      '\033[0m',          '%^RESET%^',            '<RESET>'),
    '[L': ColorToken('',    '[L',   '{L',   '&L',   '~L',   '\033[1m',      '\033[1m',          '%^BOLD%^',             '<BOLD>'),
    '[i': ColorToken('',    '[i',   '{i',   '&i',   '~i',   '\033[3m',      '\033[3m',          '%^ITALIC%^',           '<ITALIC>'),
    '[u': ColorToken('',    '[u',   '{u',   '&u',   '~u',   '\033[4m',      '\033[4m',          '%^UNDERLINE%^',        '<UNDERLINE>'),
    '[f': ColorToken('',    '[f',   '{f',   '&f',   '~$',   '\033[5m',      '\033[5m',          '%^FLASH%^',            '<FONT COLOR=BLINK>'),
    '[V': ColorToken('',    '[v',   '{v',   '&v',   '~v',   '\033[7m',      '\033[7m',          '%^REVERSE%^',          '<FONT COLOR=INVERSE>'),
    '[s': ColorToken('',    '[s',   '{s',   '&s',   '~s',   '\033[9m',      '\033[9m',          '%^STRIKETHRU%^',       '<STRIKEOUT>'),

    '[H': ColorToken('',    '[H',   '{H',   '',     '',     '\033[H',       '\033[H',           '%^HOME%^',             ''),  # Home
    '[_': ColorToken('',    '[_',   '{_',   '',     '',     '\033[K',       '\033[K',           '%^CLEARLINE%^',        ''),  # Clear to end of line
    '[@': ColorToken('',    '[@',   '{@',   '',     '',     '\033[J',       '\033[J',           '',                     ''),  # Clear to end of screen
    '[^': ColorToken('',    '[^',   '{^',   '',     '',     '\033[A',       '\033[A',           '%^CURS_UP%^',          ''),  # Cursor up
    '[v': ColorToken('',    '[v',   '{v',   '',     '',     '\033[B',       '\033[B',           '%^CURS_DOWN%^',        ''),  # Cursor down
    '[>': ColorToken('',    '[>',   '{>',   '',     '',     '\033[C',       '\033[C',           '%^CURS_RIGHT%^',       ''),  # Cursor right
    '[<': ColorToken('',    '[<',   '{<',   '',     '',     '\033[D',       '\033[D',           '%^CURS_LEFT%^',        ''),  # Cursor left

    # Background colors
    ']d': ColorToken('',    ']d',   '}d',   '^x',   '^x',   '\033[40m',     '\033[48;5;232m',   '%^B_BLACK%^',          '<COLOR BACK=\"#000000\">'),
    ']r': ColorToken('',    ']r',   '}r',   '^r',   '^r',   '\033[41m',     '\033[48;5;237m',   '%^B_RED%^',            '<COLOR BACK=\"#bb0000\">'),
    ']g': ColorToken('',    ']g',   '}g',   '^g',   '^g',   '\033[42m',     '\033[48;5;237m',   '%^B_GREEN%^',          '<COLOR BACK=\"#00bb00\">'),
    ']y': ColorToken('',    ']y',   '}y',   '^O',   '^y',   '\033[43m',     '\033[48;5;244m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#bbbb00\">'),
    ']b': ColorToken('',    ']b',   '}b',   '^b',   '^b',   '\033[44m',     '\033[48;5;237m',   '%^B_BLUE%^',           '<COLOR BACK=\"#0000bb\">'),
    ']m': ColorToken('',    ']m',   '}m',   '^p',   '^p',   '\033[45m',     '\033[48;5;244m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#bb00bb\">'),
    ']c': ColorToken('',    ']c',   '}c',   '^c',   '^c',   '\033[46m',     '\033[48;5;244m',   '%^B_CYAN%^',           '<COLOR BACK=\"#00bbbb\">'),
    ']w': ColorToken('',    ']w',   '}w',   '^w',   '^w',   '\033[47m',     '\033[48;5;250m',   '%^B_WHITE%^',          '<COLOR BACK=\"#bbbbbb\">'),

    # Background colors cannot BE bold in ANSI
    ']D': ColorToken('',    ']D',   '}D',   '^z',   '^z',   '\033[40m',     '\033[48;5;240m',   '%^B_BLACK%^',          '<COLOR BACK=\"#555555\">'),
    ']R': ColorToken('',    ']R',   '}R',   '^R',   '^R',   '\033[41m',     '\033[48;5;245m',   '%^B_RED%^',            '<COLOR BACK=\"#ff5555\">'),
    ']G': ColorToken('',    ']G',   '}G',   '^G',   '^G',   '\033[42m',     '\033[48;5;245m',   '%^B_GREEN%^',          '<COLOR BACK=\"#55ff55\">'),
    ']Y': ColorToken('',    ']Y',   '}Y',   '^Y',   '^Y',   '\033[43m',     '\033[48;5;251m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#ffff55\">'),
    ']B': ColorToken('',    ']B',   '}B',   '^B',   '^B',   '\033[44m',     '\033[48;5;245m',   '%^B_BLUE%^',           '<COLOR BACK=\"#5555ff\">'),
    ']M': ColorToken('',    ']M',   '}M',   '^P',   '^P',   '\033[45m',     '\033[48;5;251m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#ff55ff\">'),
    ']C': ColorToken('',    ']C',   '}C',   '^C',   '^C',   '\033[46m',     '\033[48;5;251m',   '%^B_CYAN%^',           '<COLOR BACK=\"#55ffff\">'),
    ']W': ColorToken('',    ']W',   '}W',   '^W',   '^W',   '\033[47m',     '\033[48;5;255m',   '%^B_WHITE%^',          '<COLOR BACK=\"#ffffff\">'),
}

COLOR_MAP['rom'] = {
    '{d': ColorToken('',    '[d',   '{d',   '&x',   '~x',   '\033[30m',     '\033[38;5;232m',   '%^BLACK%^',            '<COLOR FORE=\"#000000\">' ),
    '{r': ColorToken('',    '[r',   '{r',   '&r',   '~r',   '\033[31m',     '\033[38;5;237m',   '%^RED%^',              '<COLOR FORE=\"#bb0000\">' ),
    '{g': ColorToken('',    '[g',   '{g',   '&g',   '~g',   '\033[32m',     '\033[38;5;237m',   '%^GREEN%^',            '<COLOR FORE=\"#00bb00\">' ),
    '{y': ColorToken('',    '[y',   '{y',   '&O',   '~y',   '\033[33m',     '\033[38;5;244m',   '%^ORANGE%^',           '<COLOR FORE=\"#bbbb00\">' ),
    '{b': ColorToken('',    '[b',   '{b',   '&b',   '~b',   '\033[34m',     '\033[38;5;237m',   '%^BLUE%^',             '<COLOR FORE=\"#0000bb\">' ),
    '{m': ColorToken('',    '[m',   '{m',   '&p',   '~p',   '\033[35m',     '\033[38;5;244m',   '%^MAGENTA%^',          '<COLOR FORE=\"#bb00bb\">' ),
    '{c': ColorToken('',    '[c',   '{c',   '&c',   '~c',   '\033[36m',     '\033[38;5;244m',   '%^CYAN%^',             '<COLOR FORE=\"#00bbbb\">' ),
    '{w': ColorToken('',    '[w',   '{w',   '&w',   '~w',   '\033[37m',     '\033[38;5;250m',   '%^WHITE%^',            '<COLOR FORE=\"#bbbbbb\">' ),

    '{D': ColorToken('',    '[D',   '{D',   '&z',   '~z',   '\033[1;30m',   '\033[38;5;240m',   '%^BOLD%^BLACK%^',      '<COLOR FORE=\"#555555\">'),
    '{R': ColorToken('',    '[R',   '{R',   '&R',   '~R',   '\033[1;31m',   '\033[38;5;245m',   '%^BOLD%^RED%^',        '<COLOR FORE=\"#ff5555\">'),
    '{G': ColorToken('',    '[G',   '{G',   '&G',   '~G',   '\033[1;32m',   '\033[38;5;245m',   '%^BOLD%^GREEN%^',      '<COLOR FORE=\"#55ff55\">'),
    '{Y': ColorToken('',    '[Y',   '{Y',   '&Y',   '~Y',   '\033[1;33m',   '\033[38;5;251m',   '%^BOLD%^ORANGE%^',     '<COLOR FORE=\"#ffff55\">'),
    '{B': ColorToken('',    '[B',   '{B',   '&B',   '~B',   '\033[1;34m',   '\033[38;5;245m',   '%^BOLD%^BLUE%^',       '<COLOR FORE=\"#5555ff\">'),
    '{M': ColorToken('',    '[M',   '{M',   '&P',   '~P',   '\033[1;35m',   '\033[38;5;251m',   '%^BOLD%^MAGENTA%^',    '<COLOR FORE=\"#ff55ff\">'),
    '{C': ColorToken('',    '[C',   '{C',   '&C',   '~C',   '\033[1;36m',   '\033[38;5;251m',   '%^BOLD%^CYAN%^',       '<COLOR FORE=\"#55ffff\">'),
    '{W': ColorToken('',    '[W',   '{W',   '&W',   '~W',   '\033[1;37m',   '\033[38;5;255m',   '%^BOLD%^WHITE%^',      '<COLOR FORE=\"#ffffff\">'),

    '{*': ColorToken('',    '[*',   '{*',   '',     '',     '\007',         '\007',             '',                     ''),
    '{/': ColorToken('',    '[/',   '{/',   '',     '',     '\012',         '\012',             '',                     ''),

    '{{': ColorToken('{',   '{',    '{{',   '{',    '{',    '{',            '{',                '{',                    '{'),
    '}}': ColorToken('}',   '}',    '}}',   '}}',   '}',    '}',            '}',                '}',                    '}'),

    '{x': ColorToken('',    '[x',   '{x',   '&d',   '~!',   '\033[0m',      '\033[0m',          '%^RESET%^',            '<RESET>'),
    '{L': ColorToken('',    '[L',   '{L',   '&L',   '~L',   '\033[1m',      '\033[1m',          '%^BOLD%^',             '<BOLD>'),
    '{i': ColorToken('',    '[i',   '{i',   '&i',   '~i',   '\033[3m',      '\033[3m',          '%^ITALIC%^',           '<ITALIC>'),
    '{u': ColorToken('',    '[u',   '{u',   '&u',   '~u',   '\033[4m',      '\033[4m',          '%^UNDERLINE%^',        '<UNDERLINE>'),
    '{f': ColorToken('',    '[f',   '{f',   '&f',   '~$',   '\033[5m',      '\033[5m',          '%^FLASH%^',            '<FONT COLOR=BLINK>'),
    '{V': ColorToken('',    '[v',   '{v',   '&v',   '~v',   '\033[7m',      '\033[7m',          '%^REVERSE%^',          '<FONT COLOR=INVERSE>'),
    '{s': ColorToken('',    '[s',   '{s',   '&s',   '~s',   '\033[9m',      '\033[9m',          '%^STRIKETHRU%^',       '<STRIKEOUT>'),

    '{H': ColorToken('',    '[H',   '{H',   '',     '',     '\033[H',       '\033[H',           '%^HOME%^',             ''),  # Home
    '{_': ColorToken('',    '[_',   '{_',   '',     '',     '\033[K',       '\033[K',           '%^CLEARLINE%^',        ''),  # Clear to end of line
    '{@': ColorToken('',    '[@',   '{@',   '',     '',     '\033[J',       '\033[J',           '',                     ''),  # Clear to end of screen
    '{^': ColorToken('',    '[^',   '{^',   '',     '',     '\033[A',       '\033[A',           '%^CURS_UP%^',          ''),  # Cursor up
    '{v': ColorToken('',    '[v',   '{v',   '',     '',     '\033[B',       '\033[B',           '%^CURS_DOWN%^',        ''),  # Cursor down
    '{>': ColorToken('',    '[>',   '{>',   '',     '',     '\033[C',       '\033[C',           '%^CURS_RIGHT%^',       ''),  # Cursor right
    '{<': ColorToken('',    '[<',   '{<',   '',     '',     '\033[D',       '\033[D',           '%^CURS_LEFT%^',        ''),  # Cursor left

    # Background colors
    '}d': ColorToken('',    ']d',   '}d',   '^x',   '^x',   '\033[40m',     '\033[48;5;232m',   '%^B_BLACK%^',          '<COLOR BACK=\"#000000\">'),
    '}r': ColorToken('',    ']r',   '}r',   '^r',   '^r',   '\033[41m',     '\033[48;5;237m',   '%^B_RED%^',            '<COLOR BACK=\"#bb0000\">'),
    '}g': ColorToken('',    ']g',   '}g',   '^g',   '^g',   '\033[42m',     '\033[48;5;237m',   '%^B_GREEN%^',          '<COLOR BACK=\"#00bb00\">'),
    '}y': ColorToken('',    ']y',   '}y',   '^O',   '^y',   '\033[43m',     '\033[48;5;244m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#bbbb00\">'),
    '}b': ColorToken('',    ']b',   '}b',   '^b',   '^b',   '\033[44m',     '\033[48;5;237m',   '%^B_BLUE%^',           '<COLOR BACK=\"#0000bb\">'),
    '}m': ColorToken('',    ']m',   '}m',   '^p',   '^p',   '\033[45m',     '\033[48;5;244m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#bb00bb\">'),
    '}c': ColorToken('',    ']c',   '}c',   '^c',   '^c',   '\033[46m',     '\033[48;5;244m',   '%^B_CYAN%^',           '<COLOR BACK=\"#00bbbb\">'),
    '}w': ColorToken('',    ']w',   '}w',   '^w',   '^w',   '\033[47m',     '\033[48;5;250m',   '%^B_WHITE%^',          '<COLOR BACK=\"#bbbbbb\">'),

    # Background colors cannot BE bold in ANSI
    '}D': ColorToken('',    ']D',   '}D',   '^z',   '^z',   '\033[40m',     '\033[48;5;240m',   '%^B_BLACK%^',          '<COLOR BACK=\"#555555\">'),
    '}R': ColorToken('',    ']R',   '}R',   '^R',   '^R',   '\033[41m',     '\033[48;5;245m',   '%^B_RED%^',            '<COLOR BACK=\"#ff5555\">'),
    '}G': ColorToken('',    ']G',   '}G',   '^G',   '^G',   '\033[42m',     '\033[48;5;245m',   '%^B_GREEN%^',          '<COLOR BACK=\"#55ff55\">'),
    '}Y': ColorToken('',    ']Y',   '}Y',   '^Y',   '^Y',   '\033[43m',     '\033[48;5;251m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#ffff55\">'),
    '}B': ColorToken('',    ']B',   '}B',   '^B',   '^B',   '\033[44m',     '\033[48;5;245m',   '%^B_BLUE%^',           '<COLOR BACK=\"#5555ff\">'),
    '}M': ColorToken('',    ']M',   '}M',   '^P',   '^P',   '\033[45m',     '\033[48;5;251m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#ff55ff\">'),
    '}C': ColorToken('',    ']C',   '}C',   '^C',   '^C',   '\033[46m',     '\033[48;5;251m',   '%^B_CYAN%^',           '<COLOR BACK=\"#55ffff\">'),
    '}W': ColorToken('',    ']W',   '}W',   '^W',   '^W',   '\033[47m',     '\033[48;5;255m',   '%^B_WHITE%^',          '<COLOR BACK=\"#ffffff\">'),
}

COLOR_MAP['smaug'] = {
    '&x': ColorToken('',    '[d',   '{d',   '&x',   '~x',   '\033[30m',     '\033[38;5;232m',   '%^BLACK%^',            '<COLOR FORE=\"#000000\">' ),
    '&r': ColorToken('',    '[r',   '{r',   '&r',   '~r',   '\033[31m',     '\033[38;5;237m',   '%^RED%^',              '<COLOR FORE=\"#bb0000\">' ),
    '&g': ColorToken('',    '[g',   '{g',   '&g',   '~g',   '\033[32m',     '\033[38;5;237m',   '%^GREEN%^',            '<COLOR FORE=\"#00bb00\">' ),
    '&O': ColorToken('',    '[y',   '{y',   '&O',   '~y',   '\033[33m',     '\033[38;5;244m',   '%^ORANGE%^',           '<COLOR FORE=\"#bbbb00\">' ),
    '&b': ColorToken('',    '[b',   '{b',   '&b',   '~b',   '\033[34m',     '\033[38;5;237m',   '%^BLUE%^',             '<COLOR FORE=\"#0000bb\">' ),
    '&p': ColorToken('',    '[m',   '{m',   '&p',   '~p',   '\033[35m',     '\033[38;5;244m',   '%^MAGENTA%^',          '<COLOR FORE=\"#bb00bb\">' ),
    '&c': ColorToken('',    '[c',   '{c',   '&c',   '~c',   '\033[36m',     '\033[38;5;244m',   '%^CYAN%^',             '<COLOR FORE=\"#00bbbb\">' ),
    '&w': ColorToken('',    '[w',   '{w',   '&w',   '~w',   '\033[37m',     '\033[38;5;250m',   '%^WHITE%^',            '<COLOR FORE=\"#bbbbbb\">' ),

    '&z': ColorToken('',    '[D',   '{D',   '&z',   '~z',   '\033[1;30m',   '\033[38;5;240m',   '%^BOLD%^BLACK%^',      '<COLOR FORE=\"#555555\">'),
    '&R': ColorToken('',    '[R',   '{R',   '&R',   '~R',   '\033[1;31m',   '\033[38;5;245m',   '%^BOLD%^RED%^',        '<COLOR FORE=\"#ff5555\">'),
    '&G': ColorToken('',    '[G',   '{G',   '&G',   '~G',   '\033[1;32m',   '\033[38;5;245m',   '%^BOLD%^GREEN%^',      '<COLOR FORE=\"#55ff55\">'),
    '&Y': ColorToken('',    '[Y',   '{Y',   '&Y',   '~Y',   '\033[1;33m',   '\033[38;5;251m',   '%^BOLD%^ORANGE%^',     '<COLOR FORE=\"#ffff55\">'),
    '&B': ColorToken('',    '[B',   '{B',   '&B',   '~B',   '\033[1;34m',   '\033[38;5;245m',   '%^BOLD%^BLUE%^',       '<COLOR FORE=\"#5555ff\">'),
    '&P': ColorToken('',    '[M',   '{M',   '&P',   '~P',   '\033[1;35m',   '\033[38;5;251m',   '%^BOLD%^MAGENTA%^',    '<COLOR FORE=\"#ff55ff\">'),
    '&C': ColorToken('',    '[C',   '{C',   '&C',   '~C',   '\033[1;36m',   '\033[38;5;251m',   '%^BOLD%^CYAN%^',       '<COLOR FORE=\"#55ffff\">'),
    '&W': ColorToken('',    '[W',   '{W',   '&W',   '~W',   '\033[1;37m',   '\033[38;5;255m',   '%^BOLD%^WHITE%^',      '<COLOR FORE=\"#ffffff\">'),

    '&&': ColorToken('&',   '&',    '&',    '&&',   '&',    '&',            '&',                '&',                    '&'),
    '^^': ColorToken('^',   '^',    '^',    '^^',   '^^',   '^',            '^',                '^',                    '^'),
    '}}': ColorToken('}',   '}',    '}}',   '}}',   '}',    '}',            '}',                '}',                    '}'),

    '&d': ColorToken('',    '[x',   '{x',   '&d',   '~!',   '\033[0m',      '\033[0m',          '%^RESET%^',            '<RESET>'),
    '&L': ColorToken('',    '[L',   '{L',   '&L',   '~L',   '\033[1m',      '\033[1m',          '%^BOLD%^',             '<BOLD>'),
    '&i': ColorToken('',    '[i',   '{i',   '&i',   '~i',   '\033[3m',      '\033[3m',          '%^ITALIC%^',           '<ITALIC>'),
    '&u': ColorToken('',    '[u',   '{u',   '&u',   '~u',   '\033[4m',      '\033[4m',          '%^UNDERLINE%^',        '<UNDERLINE>'),
    '&f': ColorToken('',    '[f',   '{f',   '&f',   '~$',   '\033[5m',      '\033[5m',          '%^FLASH%^',            '<FONT COLOR=BLINK>'),
    '&v': ColorToken('',    '[v',   '{v',   '&v',   '~v',   '\033[7m',      '\033[7m',          '%^REVERSE%^',          '<FONT COLOR=INVERSE>'),
    '&s': ColorToken('',    '[s',   '{s',   '&s',   '~s',   '\033[9m',      '\033[9m',          '%^STRIKETHRU%^',       '<STRIKEOUT>'),

    '&I': ColorToken('',    '[i',   '{i',   '&i',   '~i',   '\033[3m',      '\033[3m',          '%^ITALIC%^',           '<ITALIC>'),
    '&U': ColorToken('',    '[u',   '{u',   '&u',   '~u',   '\033[4m',      '\033[4m',          '%^UNDERLINE%^',        '<UNDERLINE>'),
    '&F': ColorToken('',    '[f',   '{f',   '&f',   '~$',   '\033[5m',      '\033[5m',          '%^FLASH%^',            '<FONT COLOR=BLINK>'),
    '&V': ColorToken('',    '[v',   '{v',   '&v',   '~v',   '\033[7m',      '\033[7m',          '%^REVERSE%^',          '<FONT COLOR=INVERSE>'),
    '&S': ColorToken('',    '[s',   '{s',   '&s',   '~s',   '\033[9m',      '\033[9m',          '%^STRIKETHRU%^',       '<STRIKEOUT>'),

    # Background colors
    '^x': ColorToken('',    ']d',   '}d',   '^x',   '^x',   '\033[40m',     '\033[48;5;232m',   '%^B_BLACK%^',          '<COLOR BACK=\"#000000\">'),
    '^r': ColorToken('',    ']r',   '}r',   '^r',   '^r',   '\033[41m',     '\033[48;5;237m',   '%^B_RED%^',            '<COLOR BACK=\"#bb0000\">'),
    '^g': ColorToken('',    ']g',   '}g',   '^g',   '^g',   '\033[42m',     '\033[48;5;237m',   '%^B_GREEN%^',          '<COLOR BACK=\"#00bb00\">'),
    '^O': ColorToken('',    ']y',   '}y',   '^O',   '^y',   '\033[43m',     '\033[48;5;244m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#bbbb00\">'),
    '^b': ColorToken('',    ']b',   '}b',   '^b',   '^b',   '\033[44m',     '\033[48;5;237m',   '%^B_BLUE%^',           '<COLOR BACK=\"#0000bb\">'),
    '^p': ColorToken('',    ']m',   '}m',   '^p',   '^p',   '\033[45m',     '\033[48;5;244m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#bb00bb\">'),
    '^c': ColorToken('',    ']c',   '}c',   '^c',   '^c',   '\033[46m',     '\033[48;5;244m',   '%^B_CYAN%^',           '<COLOR BACK=\"#00bbbb\">'),
    '^w': ColorToken('',    ']w',   '}w',   '^w',   '^w',   '\033[47m',     '\033[48;5;250m',   '%^B_WHITE%^',          '<COLOR BACK=\"#bbbbbb\">'),

    # Background colors cannot BE bold in ANSI
    '^z': ColorToken('',    ']D',   '}D',   '^z',   '^z',   '\033[40m',     '\033[48;5;240m',   '%^B_BLACK%^',          '<COLOR BACK=\"#555555\">'),
    '^R': ColorToken('',    ']R',   '}R',   '^R',   '^R',   '\033[41m',     '\033[48;5;245m',   '%^B_RED%^',            '<COLOR BACK=\"#ff5555\">'),
    '^G': ColorToken('',    ']G',   '}G',   '^G',   '^G',   '\033[42m',     '\033[48;5;245m',   '%^B_GREEN%^',          '<COLOR BACK=\"#55ff55\">'),
    '^Y': ColorToken('',    ']Y',   '}Y',   '^Y',   '^Y',   '\033[43m',     '\033[48;5;251m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#ffff55\">'),
    '^B': ColorToken('',    ']B',   '}B',   '^B',   '^B',   '\033[44m',     '\033[48;5;245m',   '%^B_BLUE%^',           '<COLOR BACK=\"#5555ff\">'),
    '^P': ColorToken('',    ']M',   '}M',   '^P',   '^P',   '\033[45m',     '\033[48;5;251m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#ff55ff\">'),
    '^C': ColorToken('',    ']C',   '}C',   '^C',   '^C',   '\033[46m',     '\033[48;5;251m',   '%^B_CYAN%^',           '<COLOR BACK=\"#55ffff\">'),
    '^W': ColorToken('',    ']W',   '}W',   '^W',   '^W',   '\033[47m',     '\033[48;5;255m',   '%^B_WHITE%^',          '<COLOR BACK=\"#ffffff\">'),

    # Blinking colors
    '}x': ColorToken('',    '[f[d', '{f{d', '}x',   '`x',   '\033[5;30m',   '\033[5;38;5;232m', '%^FLASH%^BLACK%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#000000\">'),
    '}r': ColorToken('',    '[f[r', '{f{r', '}r',   '`r',   '\033[5;31m',   '\033[5;38;5;237m', '%^FLASH%^RED%^',       '<FONT COLOR=BLINK><COLOR FORE=\"#bb0000\">'),
    '}g': ColorToken('',    '[f[g', '{f{g', '}g',   '`g',   '\033[5;32m',   '\033[5;38;5;237m', '%^FLASH%^GREEN%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#00bb00\">'),
    '}O': ColorToken('',    '[f[y', '{f{y', '}O',   '`y',   '\033[5;33m',   '\033[5;38;5;244m', '%^FLASH%^ORANGE%^',    '<FONT COLOR=BLINK><COLOR FORE=\"#bbbb00\">'),
    '}b': ColorToken('',    '[f[b', '{f{b', '}b',   '`b',   '\033[5;34m',   '\033[5;38;5;237m', '%^FLASH%^BLUE%^',      '<FONT COLOR=BLINK><COLOR FORE=\"#0000bb\">'),
    '}p': ColorToken('',    '[f[m', '{f{m', '}p',   '`p',   '\033[5;35m',   '\033[5;38;5;244m', '%^FLASH%^MAGENTA%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#bb00bb\">'),
    '}c': ColorToken('',    '[f[c', '{f{c', '}c',   '`c',   '\033[5;36m',   '\033[5;38;5;244m', '%^FLASH%^CYAN%^',      '<FONT COLOR=BLINK><COLOR FORE=\"#00bbbb\">'),
    '}w': ColorToken('',    '[f[w', '{f{w', '}w',   '`w',   '\033[5;37m',   '\033[5;38;5;250m', '%^FLASH%^WHITE%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#bbbbbb\">'),

    '}z': ColorToken('',    ']f]D', '{f{D', '}z',   '`z',   '\033[5;1;30m', '\033[5;38;5;240m', '%^FLASH%^BOLD%^BLACK%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#555555\">'),
    '}R': ColorToken('',    ']f]R', '{f{R', '}R',   '`R',   '\033[5;1;31m', '\033[5;38;5;245m', '%^FLASH%^BOLD%^RED%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#ff5555\">'),
    '}G': ColorToken('',    ']f]G', '{f{G', '}G',   '`G',   '\033[5;1;32m', '\033[5;38;5;245m', '%^FLASH%^BOLD%^GREEN%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#55ff55\">'),
    '}Y': ColorToken('',    ']f]Y', '{f{Y', '}Y',   '`Y',   '\033[5;1;33m', '\033[5;38;5;251m', '%^FLASH%^BOLD%^ORANGE%^',  '<FONT COLOR=BLINK><COLOR FORE=\"#ffff55\">'),
    '}B': ColorToken('',    ']f]B', '{f{B', '}B',   '`B',   '\033[5;1;34m', '\033[5;38;5;245m', '%^FLASH%^BOLD%^BLUE%^',    '<FONT COLOR=BLINK><COLOR FORE=\"#5555ff\">'),
    '}P': ColorToken('',    ']f]M', '{f{M', '}P',   '`P',   '\033[5;1;35m', '\033[5;38;5;251m', '%^FLASH%^BOLD%^MAGENTA%^', '<FONT COLOR=BLINK><COLOR FORE=\"#ff55ff\">'),
    '}C': ColorToken('',    ']f]C', '{f{C', '}C',   '`C',   '\033[5;1;36m', '\033[5;38;5;251m', '%^FLASH%^BOLD%^CYAN%^',    '<FONT COLOR=BLINK><COLOR FORE=\"#55ffff\">'),
    '}W': ColorToken('',    ']f]W', '{f{W', '}W',   '`W',   '\033[5;1;37m', '\033[5;38;5;255m', '%^FLASH%^BOLD%^WHITE%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#ffffff\">'),
}

COLOR_MAP['i3'] = {
    'BLACK':        ColorToken('', '[d', '{d', '&x', '~x', '\033[30m',      '\033[38;5;232m',   '%^BLACK%^',        '<COLOR FORE=\"#000000\">'),
    'RED':          ColorToken('', '[r', '{r', '&r', '~r', '\033[31m',      '\033[38;5;237m',   '%^RED%^',          '<COLOR FORE=\"#bb0000\">'),
    'GREEN':        ColorToken('', '[g', '{g', '&g', '~g', '\033[32m',      '\033[38;5;237m',   '%^GREEN%^',        '<COLOR FORE=\"#00bb00\">'),
    'ORANGE':       ColorToken('', '[y', '{y', '&O', '~y', '\033[33m',      '\033[38;5;244m',   '%^ORANGE%^',       '<COLOR FORE=\"#bbbb00\">'),
    'BLUE':         ColorToken('', '[b', '{b', '&b', '~b', '\033[34m',      '\033[38;5;237m',   '%^BLUE%^',         '<COLOR FORE=\"#0000bb\">'),
    'MAGENTA':      ColorToken('', '[m', '{m', '&p', '~p', '\033[35m',      '\033[38;5;244m',   '%^MAGENTA%^',      '<COLOR FORE=\"#bb00bb\">'),
    'CYAN':         ColorToken('', '[c', '{c', '&c', '~c', '\033[36m',      '\033[38;5;244m',   '%^CYAN%^',         '<COLOR FORE=\"#00bbbb\">'),
    'WHITE':        ColorToken('', '[w', '{w', '&w', '~w', '\033[37m',      '\033[38;5;250m',   '%^WHITE%^',        '<COLOR FORE=\"#bbbbbb\">'),
    'YELLOW':       ColorToken('', '[Y', '{Y', '&Y', '~Y', '\033[1;33m',    '\033[38;5;251m',   '%^BOLD%^ORANGE%^', '<COLOR FORE=\"#ffff55\">'),

    'RESET':        ColorToken('', '[x', '{x', '&d', '~!', '\033[0m',       '\033[0m',          '%^RESET%^',        '<RESET>'),
    'BOLD':         ColorToken('', '[L', '{L', '&L', '~L', '\033[1m',       '\033[1m',          '%^BOLD%^',         '<BOLD>'),
    'ITALIC':       ColorToken('', '[i', '{i', '&i', '~i', '\033[3m',       '\033[3m',          '%^ITALIC%^',       '<ITALIC>'),
    'UNDERLINE':    ColorToken('', '[u', '{u', '&u', '~u', '\033[4m',       '\033[4m',          '%^UNDERLINE%^',    '<UNDERLINE>'),
    'FLASH':        ColorToken('', '[f', '{f', '&f', '~$', '\033[5m',       '\033[5m',          '%^FLASH%^',        '<FONT COLOR=BLINK>'),
    'REVERSE':      ColorToken('', '[v', '{v', '&v', '~v', '\033[7m',       '\033[7m',          '%^REVERSE%^',      '<FONT COLOR=INVERSE>'),
    'STRIKETHRU':   ColorToken('', '[s', '{s', '&s', '~s', '\033[9m',       '\033[9m',          '%^STRIKETHRU%^',   '<STRIKEOUT>'),

    'HOME':         ColorToken('', '[H', '{H', '', '', '\033[H', '\033[H', '%^HOME%^',          ''),  # Home
    'CLEARLINE':    ColorToken('', '[_', '{_', '', '', '\033[K', '\033[K', '%^CLEARLINE%^',     ''),  # Clear to end of line
    'CURS_UP':      ColorToken('', '[^', '{^', '', '', '\033[A', '\033[A', '%^CURS_UP%^',       ''),  # Cursor up
    'CURS_DOWN':    ColorToken('', '[v', '{v', '', '', '\033[B', '\033[B', '%^CURS_DOWN%^',     ''),  # Cursor down
    'CURS_RIGHT':   ColorToken('', '[>', '{>', '', '', '\033[C', '\033[C', '%^CURS_RIGHT%^',    ''),  # Cursor right
    'CURS_LEFT':    ColorToken('', '[<', '{<', '', '', '\033[D', '\033[D', '%^CURS_LEFT%^',     ''),  # Cursor left

    'B_BLACK':      ColorToken('', ']d', '}d', '^x', '^x', '\033[40m', '\033[48;5;232m', '%^B_BLACK%^',   '<COLOR BACK=\"#000000\">'),
    'B_RED':        ColorToken('', ']r', '}r', '^r', '^r', '\033[41m', '\033[48;5;237m', '%^B_RED%^',     '<COLOR BACK=\"#bb0000\">'),
    'B_GREEN':      ColorToken('', ']g', '}g', '^g', '^g', '\033[42m', '\033[48;5;237m', '%^B_GREEN%^',   '<COLOR BACK=\"#00bb00\">'),
    'B_ORANGE':     ColorToken('', ']y', '}y', '^O', '^y', '\033[43m', '\033[48;5;244m', '%^B_ORANGE%^',  '<COLOR BACK=\"#bbbb00\">'),
    'B_BLUE':       ColorToken('', ']b', '}b', '^b', '^b', '\033[44m', '\033[48;5;237m', '%^B_BLUE%^',    '<COLOR BACK=\"#0000bb\">'),
    'B_MAGENTA':    ColorToken('', ']m', '}m', '^p', '^p', '\033[45m', '\033[48;5;244m', '%^B_MAGENTA%^', '<COLOR BACK=\"#bb00bb\">'),
    'B_CYAN':       ColorToken('', ']c', '}c', '^c', '^c', '\033[46m', '\033[48;5;244m', '%^B_CYAN%^',    '<COLOR BACK=\"#00bbbb\">'),
    'B_WHITE':      ColorToken('', ']w', '}w', '^w', '^w', '\033[47m', '\033[48;5;250m', '%^B_WHITE%^',   '<COLOR BACK=\"#bbbbbb\">'),
    'B_YELLOW':     ColorToken('', ']Y', '}Y', '^Y', '^Y', '\033[43m', '\033[48;5;251m', '%^B_ORANGE%^',  '<COLOR BACK=\"#ffff55\">'),
}

COLOR_MAP['imc2'] = {
    '~x': ColorToken('',    '[d',   '{d',   '&x',   '~x',   '\033[30m',     '\033[38;5;232m',   '%^BLACK%^',            '<COLOR FORE=\"#000000\">' ),
    '~r': ColorToken('',    '[r',   '{r',   '&r',   '~r',   '\033[31m',     '\033[38;5;237m',   '%^RED%^',              '<COLOR FORE=\"#bb0000\">' ),
    '~g': ColorToken('',    '[g',   '{g',   '&g',   '~g',   '\033[32m',     '\033[38;5;237m',   '%^GREEN%^',            '<COLOR FORE=\"#00bb00\">' ),
    '~y': ColorToken('',    '[y',   '{y',   '&O',   '~y',   '\033[33m',     '\033[38;5;244m',   '%^ORANGE%^',           '<COLOR FORE=\"#bbbb00\">' ),
    '~b': ColorToken('',    '[b',   '{b',   '&b',   '~b',   '\033[34m',     '\033[38;5;237m',   '%^BLUE%^',             '<COLOR FORE=\"#0000bb\">' ),
    '~p': ColorToken('',    '[m',   '{m',   '&p',   '~p',   '\033[35m',     '\033[38;5;244m',   '%^MAGENTA%^',          '<COLOR FORE=\"#bb00bb\">' ),
    '~c': ColorToken('',    '[c',   '{c',   '&c',   '~c',   '\033[36m',     '\033[38;5;244m',   '%^CYAN%^',             '<COLOR FORE=\"#00bbbb\">' ),
    '~w': ColorToken('',    '[w',   '{w',   '&w',   '~w',   '\033[37m',     '\033[38;5;250m',   '%^WHITE%^',            '<COLOR FORE=\"#bbbbbb\">' ),

    '~z': ColorToken('',    '[D',   '{D',   '&z',   '~z',   '\033[1;30m',   '\033[38;5;240m',   '%^BOLD%^BLACK%^',      '<COLOR FORE=\"#555555\">'),
    '~R': ColorToken('',    '[R',   '{R',   '&R',   '~R',   '\033[1;31m',   '\033[38;5;245m',   '%^BOLD%^RED%^',        '<COLOR FORE=\"#ff5555\">'),
    '~G': ColorToken('',    '[G',   '{G',   '&G',   '~G',   '\033[1;32m',   '\033[38;5;245m',   '%^BOLD%^GREEN%^',      '<COLOR FORE=\"#55ff55\">'),
    '~Y': ColorToken('',    '[Y',   '{Y',   '&Y',   '~Y',   '\033[1;33m',   '\033[38;5;251m',   '%^BOLD%^ORANGE%^',     '<COLOR FORE=\"#ffff55\">'),
    '~B': ColorToken('',    '[B',   '{B',   '&B',   '~B',   '\033[1;34m',   '\033[38;5;245m',   '%^BOLD%^BLUE%^',       '<COLOR FORE=\"#5555ff\">'),
    '~P': ColorToken('',    '[M',   '{M',   '&P',   '~P',   '\033[1;35m',   '\033[38;5;251m',   '%^BOLD%^MAGENTA%^',    '<COLOR FORE=\"#ff55ff\">'),
    '~C': ColorToken('',    '[C',   '{C',   '&C',   '~C',   '\033[1;36m',   '\033[38;5;251m',   '%^BOLD%^CYAN%^',       '<COLOR FORE=\"#55ffff\">'),
    '~W': ColorToken('',    '[W',   '{W',   '&W',   '~W',   '\033[1;37m',   '\033[38;5;255m',   '%^BOLD%^WHITE%^',      '<COLOR FORE=\"#ffffff\">'),

    '~~': ColorToken('~',   '~',    '~',    '~',    '~~',   '~',            '~',                '~',                    '~'),
    '^^': ColorToken('^',   '^',    '^',    '^^',   '^^',   '^',            '^',                '^',                    '^'),
    '``': ColorToken('`',   '`',    '`',    '`',    '``',   '`',            '`',                '`',                    '`'),

    '~!': ColorToken('',    '[x',   '{x',   '&d',   '~!',   '\033[0m',      '\033[0m',          '%^RESET%^',            '<RESET>'),
    '~L': ColorToken('',    '[L',   '{L',   '&L',   '~L',   '\033[1m',      '\033[1m',          '%^BOLD%^',             '<BOLD>'),
    '~i': ColorToken('',    '[i',   '{i',   '&i',   '~i',   '\033[3m',      '\033[3m',          '%^ITALIC%^',           '<ITALIC>'),
    '~u': ColorToken('',    '[u',   '{u',   '&u',   '~u',   '\033[4m',      '\033[4m',          '%^UNDERLINE%^',        '<UNDERLINE>'),
    '~$': ColorToken('',    '[f',   '{f',   '&f',   '~$',   '\033[5m',      '\033[5m',          '%^FLASH%^',            '<FONT COLOR=BLINK>'),
    '~v': ColorToken('',    '[v',   '{v',   '&v',   '~v',   '\033[7m',      '\033[7m',          '%^REVERSE%^',          '<FONT COLOR=INVERSE>'),
    '~s': ColorToken('',    '[s',   '{s',   '&s',   '~s',   '\033[9m',      '\033[9m',          '%^STRIKETHRU%^',       '<STRIKEOUT>'),

    '~Z': ColorToken('',    '',     '',     '&Z',   '~Z',   '',             '',                 '',                     ''),  # Random foreground
    '~D': ColorToken('',    '[D',   '{D',   '&z',   '~z',   '\033[1;30m',   '\033[38;5;240m',   '%^BOLD%^BLACK%^',      '<COLOR FORE=\"#555555\">'),
    '~m': ColorToken('',    '[m',   '{m',   '&p',   '~p',   '\033[35m',     '\033[38;5;244m',   '%^MAGENTA%^',          '<COLOR FORE=\"#bb00bb\">'),
    '~d': ColorToken('',    '[w',   '{w',   '&w',   '~w',   '\033[37m',     '\033[38;5;250m',   '%^WHITE%^',            '<COLOR FORE=\"#bbbbbb\">'),
    '~M': ColorToken('',    '[M',   '{M',   '&P',   '~P',   '\033[1;35m',   '\033[38;5;251m',   '%^BOLD%^MAGENTA%^',    '<COLOR FORE=\"#ff55ff\">'),

    # Background colors
    '^x': ColorToken('',    ']d',   '}d',   '^x',   '^x',   '\033[40m',     '\033[48;5;232m',   '%^B_BLACK%^',          '<COLOR BACK=\"#000000\">'),
    '^r': ColorToken('',    ']r',   '}r',   '^r',   '^r',   '\033[41m',     '\033[48;5;237m',   '%^B_RED%^',            '<COLOR BACK=\"#bb0000\">'),
    '^g': ColorToken('',    ']g',   '}g',   '^g',   '^g',   '\033[42m',     '\033[48;5;237m',   '%^B_GREEN%^',          '<COLOR BACK=\"#00bb00\">'),
    '^y': ColorToken('',    ']y',   '}y',   '^O',   '^y',   '\033[43m',     '\033[48;5;244m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#bbbb00\">'),
    '^b': ColorToken('',    ']b',   '}b',   '^b',   '^b',   '\033[44m',     '\033[48;5;237m',   '%^B_BLUE%^',           '<COLOR BACK=\"#0000bb\">'),
    '^p': ColorToken('',    ']m',   '}m',   '^p',   '^p',   '\033[45m',     '\033[48;5;244m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#bb00bb\">'),
    '^c': ColorToken('',    ']c',   '}c',   '^c',   '^c',   '\033[46m',     '\033[48;5;244m',   '%^B_CYAN%^',           '<COLOR BACK=\"#00bbbb\">'),
    '^w': ColorToken('',    ']w',   '}w',   '^w',   '^w',   '\033[47m',     '\033[48;5;250m',   '%^B_WHITE%^',          '<COLOR BACK=\"#bbbbbb\">'),

    # Background colors cannot BE bold in ANSI
    '^z': ColorToken('',    ']D',   '}D',   '^z',   '^z',   '\033[40m',     '\033[48;5;240m',   '%^B_BLACK%^',          '<COLOR BACK=\"#555555\">'),
    '^R': ColorToken('',    ']R',   '}R',   '^R',   '^R',   '\033[41m',     '\033[48;5;245m',   '%^B_RED%^',            '<COLOR BACK=\"#ff5555\">'),
    '^G': ColorToken('',    ']G',   '}G',   '^G',   '^G',   '\033[42m',     '\033[48;5;245m',   '%^B_GREEN%^',          '<COLOR BACK=\"#55ff55\">'),
    '^Y': ColorToken('',    ']Y',   '}Y',   '^Y',   '^Y',   '\033[43m',     '\033[48;5;251m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#ffff55\">'),
    '^B': ColorToken('',    ']B',   '}B',   '^B',   '^B',   '\033[44m',     '\033[48;5;245m',   '%^B_BLUE%^',           '<COLOR BACK=\"#5555ff\">'),
    '^P': ColorToken('',    ']M',   '}M',   '^P',   '^P',   '\033[45m',     '\033[48;5;251m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#ff55ff\">'),
    '^C': ColorToken('',    ']C',   '}C',   '^C',   '^C',   '\033[46m',     '\033[48;5;251m',   '%^B_CYAN%^',           '<COLOR BACK=\"#55ffff\">'),
    '^W': ColorToken('',    ']W',   '}W',   '^W',   '^W',   '\033[47m',     '\033[48;5;255m',   '%^B_WHITE%^',          '<COLOR BACK=\"#ffffff\">'),

    '^D': ColorToken('',    ']D',   '}D',   '^z',   '^z',   '\033[40m',     '\033[48;5;232m',   '%^B_BLACK%^',          '<COLOR BACK=\"#555555\">'),
    '^m': ColorToken('',    ']m',   '}m',   '^p',   '^p',   '\033[45m',     '\033[48;5;244m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#bb00bb\">'),
    '^d': ColorToken('',    ']w',   '}w',   '^w',   '^w',   '\033[47m',     '\033[48;5;250m',   '%^B_WHITE%^',          '<COLOR BACK=\"#bbbbbb\">'),
    '^M': ColorToken('',    ']M',   '}M',   '^P',   '^P',   '\033[45m',     '\033[48;5;244m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#ff55ff\">'),

    # Blinking colors
    '`x': ColorToken('',    '[f[d', '{f{d', '}x',   '`x',   '\033[5;30m',   '\033[5;38;5;232m', '%^FLASH%^BLACK%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#000000\">'),
    '`r': ColorToken('',    '[f[r', '{f{r', '}r',   '`r',   '\033[5;31m',   '\033[5;38;5;237m', '%^FLASH%^RED%^',       '<FONT COLOR=BLINK><COLOR FORE=\"#bb0000\">'),
    '`g': ColorToken('',    '[f[g', '{f{g', '}g',   '`g',   '\033[5;32m',   '\033[5;38;5;237m', '%^FLASH%^GREEN%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#00bb00\">'),
    '`y': ColorToken('',    '[f[y', '{f{y', '}O',   '`y',   '\033[5;33m',   '\033[5;38;5;244m', '%^FLASH%^ORANGE%^',    '<FONT COLOR=BLINK><COLOR FORE=\"#bbbb00\">'),
    '`b': ColorToken('',    '[f[b', '{f{b', '}b',   '`b',   '\033[5;34m',   '\033[5;38;5;237m', '%^FLASH%^BLUE%^',      '<FONT COLOR=BLINK><COLOR FORE=\"#0000bb\">'),
    '`p': ColorToken('',    '[f[m', '{f{m', '}p',   '`p',   '\033[5;35m',   '\033[5;38;5;244m', '%^FLASH%^MAGENTA%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#bb00bb\">'),
    '`c': ColorToken('',    '[f[c', '{f{c', '}c',   '`c',   '\033[5;36m',   '\033[5;38;5;244m', '%^FLASH%^CYAN%^',      '<FONT COLOR=BLINK><COLOR FORE=\"#00bbbb\">'),
    '`w': ColorToken('',    '[f[w', '{f{w', '}w',   '`w',   '\033[5;37m',   '\033[5;38;5;250m', '%^FLASH%^WHITE%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#bbbbbb\">'),

    '`z': ColorToken('',    ']f]D', '{f{D', '}z',   '`z',   '\033[5;1;30m', '\033[5;38;5;240m', '%^FLASH%^BOLD%^BLACK%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#555555\">'),
    '`R': ColorToken('',    ']f]R', '{f{R', '}R',   '`R',   '\033[5;1;31m', '\033[5;38;5;245m', '%^FLASH%^BOLD%^RED%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#ff5555\">'),
    '`G': ColorToken('',    ']f]G', '{f{G', '}G',   '`G',   '\033[5;1;32m', '\033[5;38;5;245m', '%^FLASH%^BOLD%^GREEN%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#55ff55\">'),
    '`Y': ColorToken('',    ']f]Y', '{f{Y', '}Y',   '`Y',   '\033[5;1;33m', '\033[5;38;5;251m', '%^FLASH%^BOLD%^ORANGE%^',  '<FONT COLOR=BLINK><COLOR FORE=\"#ffff55\">'),
    '`B': ColorToken('',    ']f]B', '{f{B', '}B',   '`B',   '\033[5;1;34m', '\033[5;38;5;245m', '%^FLASH%^BOLD%^BLUE%^',    '<FONT COLOR=BLINK><COLOR FORE=\"#5555ff\">'),
    '`P': ColorToken('',    ']f]M', '{f{M', '}P',   '`P',   '\033[5;1;35m', '\033[5;38;5;251m', '%^FLASH%^BOLD%^MAGENTA%^', '<FONT COLOR=BLINK><COLOR FORE=\"#ff55ff\">'),
    '`C': ColorToken('',    ']f]C', '{f{C', '}C',   '`C',   '\033[5;1;36m', '\033[5;38;5;251m', '%^FLASH%^BOLD%^CYAN%^',    '<FONT COLOR=BLINK><COLOR FORE=\"#55ffff\">'),
    '`W': ColorToken('',    ']f]W', '{f{W', '}W',   '`W',   '\033[5;1;37m', '\033[5;38;5;255m', '%^FLASH%^BOLD%^WHITE%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#ffffff\">'),

    '`D': ColorToken('',    '[f[D', '{f{D', '}z',   '`z',   '\033[5;1;30m', '\033[5;48;5;232m', '%^FLASH%^BOLD%^B_BLACK%^',  '<FONT COLOR=BLINK><COLOR FORE=\"#555555\">'),
    '`m': ColorToken('',    '[f[m', '{f{m', '}p',   '`p',   '\033[5;35m',   '\033[5;48;5;244m', '%^FLASH%^MAGENTA%^',        '<FONT COLOR=BLINK><COLOR FORE=\"#bb00bb\">'),
    '`d': ColorToken('',    '[f[w', '{f{w', '}w',   '`w',   '\033[5;37m',   '\033[5;48;5;250m', '%^FLASH%^WHITE%^',          '<FONT COLOR=BLINK><COLOR FORE=\"#bbbbbb\">'),
    '`M': ColorToken('',    '[f[M', '{f{M', '}P',   '`P',   '\033[5;1;35m', '\033[5;48;5;244m', '%^FLASH%^BOLD%^MAGENTA%^',  '<FONT COLOR=BLINK><COLOR FORE=\"#ff55ff\">'),
}
