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

TERMINAL_TYPES = ('unknown', 'pyom', 'rom', 'smaug', 'imc2', 'i3', 'ansi', 'mxp')

ColorToken = namedtuple('ColorToken', TERMINAL_TYPES)

COLOR_MAP = {}

COLOR_MAP['unknown'] = {
}

COLOR_MAP['pyom'] = {
    '[d': ColorToken('', '[d', '{d', '&x', '~x', '%^BLACK%^', '\033[30m', '<COLOR FORE=\"#000000\">'),
    '[r': ColorToken('', '[r', '{r', '&r', '~r', '%^RED%^', '\033[31m', '<COLOR FORE=\"#bb0000\">'),
    '[g': ColorToken('', '[g', '{g', '&g', '~g', '%^GREEN%^', '\033[32m', '<COLOR FORE=\"#00bb00\">'),
    '[y': ColorToken('', '[y', '{y', '&O', '~y', '%^ORANGE%^', '\033[33m', '<COLOR FORE=\"#bbbb00\">'),
    '[b': ColorToken('', '[b', '{b', '&b', '~b', '%^BLUE%^', '\033[34m', '<COLOR FORE=\"#0000bb\">'),
    '[m': ColorToken('', '[m', '{m', '&p', '~p', '%^MAGENTA%^', '\033[35m', '<COLOR FORE=\"#bb00bb\">'),
    '[c': ColorToken('', '[c', '{c', '&c', '~c', '%^CYAN%^', '\033[36m', '<COLOR FORE=\"#00bbbb\">'),
    '[w': ColorToken('', '[w', '{w', '&w', '~w', '%^WHITE%^', '\033[37m', '<COLOR FORE=\"#bbbbbb\">'),

    '[D': ColorToken('', '[D', '{D', '&z', '~z', '%^BOLD%^BLACK%^', '\033[1;30m', '<COLOR FORE=\"#555555\">'),
    '[R': ColorToken('', '[R', '{R', '&R', '~R', '%^BOLD%^RED%^', '\033[1;31m', '<COLOR FORE=\"#ff5555\">'),
    '[G': ColorToken('', '[G', '{G', '&G', '~G', '%^BOLD%^GREEN%^', '\033[1;32m', '<COLOR FORE=\"#55ff55\">'),
    '[Y': ColorToken('', '[Y', '{Y', '&Y', '~Y', '%^BOLD%^ORANGE%^', '\033[1;33m', '<COLOR FORE=\"#ffff55\">'),
    '[B': ColorToken('', '[B', '{B', '&B', '~B', '%^BOLD%^BLUE%^', '\033[1;34m', '<COLOR FORE=\"#5555ff\">'),
    '[M': ColorToken('', '[M', '{M', '&P', '~P', '%^BOLD%^MAGENTA%^', '\033[1;35m', '<COLOR FORE=\"#ff55ff\">'),
    '[C': ColorToken('', '[C', '{C', '&C', '~C', '%^BOLD%^CYAN%^', '\033[1;36m', '<COLOR FORE=\"#55ffff\">'),
    '[W': ColorToken('', '[W', '{W', '&W', '~W', '%^BOLD%^WHITE%^', '\033[1;37m', '<COLOR FORE=\"#ffffff\">'),

    '[*': ColorToken('', '[*', '{*', '', '', '', '\007', ''),
    '[/': ColorToken('', '[/', '{/', '', '', '', '\012', ''),

    '[[': ColorToken('[', '[[', '[', '[', '[', '[', '[', '['),
    ']]': ColorToken(']', ']]', ']', ']', ']', ']', ']', ']'),

    '[x': ColorToken('', '[x', '{x', '&d', '~!', '%^RESET%^', '\033[0m', '<RESET>'),
    '[L': ColorToken('', '[L', '{L', '&L', '~L', '%^BOLD%^', '\033[1m', '<BOLD>'),
    '[i': ColorToken('', '[i', '{i', '&i', '~i', '%^ITALIC%^', '\033[3m', '<ITALIC>'),
    '[u': ColorToken('', '[u', '{u', '&u', '~u', '%^UNDERLINE%^', '\033[4m', '<UNDERLINE>'),
    '[f': ColorToken('', '[f', '{f', '&f', '~$', '%^FLASH%^', '\033[5m', '<FONT COLOR=BLINK>'),
    '[V': ColorToken('', '[v', '{v', '&v', '~v', '%^REVERSE%^', '\033[7m', '<FONT COLOR=INVERSE>'),
    '[s': ColorToken('', '[s', '{s', '&s', '~s', '%^STRIKETHRU%^', '\033[9m', '<STRIKEOUT>'),

    '[H': ColorToken('', '[H', '{H', '', '', '%^HOME%^', '\033[H', ''),  # Home
    '[_': ColorToken('', '[_', '{_', '', '', '%^CLEARLINE%^', '\033[K', ''),  # Clear to end of line
    '[@': ColorToken('', '[@', '{@', '', '', '', '\033[J', ''),  # Clear to end of screen
    '[^': ColorToken('', '[^', '{^', '', '', '%^CURS_UP%^', '\033[A', ''),  # Cursor up
    '[v': ColorToken('', '[v', '{v', '', '', '%^CURS_DOWN%^', '\033[B', ''),  # Cursor down
    '[>': ColorToken('', '[>', '{>', '', '', '%^CURS_RIGHT%^', '\033[C', ''),  # Cursor right
    '[<': ColorToken('', '[<', '{<', '', '', '%^CURS_LEFT%^', '\033[D', ''),  # Cursor left

    # Background colors
    ']d': ColorToken('', ']d', '}d', '^x', '^x', '%^B_BLACK%^', '\033[40m', '<COLOR BACK=\"#000000\">'),
    ']r': ColorToken('', ']r', '}r', '^r', '^r', '%^B_RED%^', '\033[41m', '<COLOR BACK=\"#bb0000\">'),
    ']g': ColorToken('', ']g', '}g', '^g', '^g', '%^B_GREEN%^', '\033[42m', '<COLOR BACK=\"#00bb00\">'),
    ']y': ColorToken('', ']y', '}y', '^O', '^y', '%^B_ORANGE%^', '\033[43m', '<COLOR BACK=\"#bbbb00\">'),
    ']b': ColorToken('', ']b', '}b', '^b', '^b', '%^B_BLUE%^', '\033[44m', '<COLOR BACK=\"#0000bb\">'),
    ']m': ColorToken('', ']m', '}m', '^p', '^p', '%^B_MAGENTA%^', '\033[45m', '<COLOR BACK=\"#bb00bb\">'),
    ']c': ColorToken('', ']c', '}c', '^c', '^c', '%^B_CYAN%^', '\033[46m', '<COLOR BACK=\"#00bbbb\">'),
    ']w': ColorToken('', ']w', '}w', '^w', '^w', '%^B_WHITE%^', '\033[47m', '<COLOR BACK=\"#bbbbbb\">'),

    # Background colors cannot BE bold in ANSI
    ']D': ColorToken('', ']D', '}D', '^z', '^z', '%^B_BLACK%^', '\033[40m', '<COLOR BACK=\"#555555\">'),
    ']R': ColorToken('', ']R', '}R', '^R', '^R', '%^B_RED%^', '\033[41m', '<COLOR BACK=\"#ff5555\">'),
    ']G': ColorToken('', ']G', '}G', '^G', '^G', '%^B_GREEN%^', '\033[42m', '<COLOR BACK=\"#55ff55\">'),
    ']Y': ColorToken('', ']Y', '}Y', '^Y', '^Y', '%^B_ORANGE%^', '\033[43m', '<COLOR BACK=\"#ffff55\">'),
    ']B': ColorToken('', ']B', '}B', '^B', '^B', '%^B_BLUE%^', '\033[44m', '<COLOR BACK=\"#5555ff\">'),
    ']M': ColorToken('', ']M', '}M', '^P', '^P', '%^B_MAGENTA%^', '\033[45m', '<COLOR BACK=\"#ff55ff\">'),
    ']C': ColorToken('', ']C', '}C', '^C', '^C', '%^B_CYAN%^', '\033[46m', '<COLOR BACK=\"#55ffff\">'),
    ']W': ColorToken('', ']W', '}W', '^W', '^W', '%^B_WHITE%^', '\033[47m', '<COLOR BACK=\"#ffffff\">'),
}

COLOR_MAP['rom'] = {
    '{d': ColorToken('', '[d', '{d', '&x', '~x', '%^BLACK%^', '\033[30m', '<COLOR FORE=\"#000000\">'),
    '{r': ColorToken('', '[r', '{r', '&r', '~r', '%^RED%^', '\033[31m', '<COLOR FORE=\"#bb0000\">'),
    '{g': ColorToken('', '[g', '{g', '&g', '~g', '%^GREEN%^', '\033[32m', '<COLOR FORE=\"#00bb00\">'),
    '{y': ColorToken('', '[y', '{y', '&O', '~y', '%^ORANGE%^', '\033[33m', '<COLOR FORE=\"#bbbb00\">'),
    '{b': ColorToken('', '[b', '{b', '&b', '~b', '%^BLUE%^', '\033[34m', '<COLOR FORE=\"#0000bb\">'),
    '{m': ColorToken('', '[m', '{m', '&p', '~p', '%^MAGENTA%^', '\033[35m', '<COLOR FORE=\"#bb00bb\">'),
    '{c': ColorToken('', '[c', '{c', '&c', '~c', '%^CYAN%^', '\033[36m', '<COLOR FORE=\"#00bbbb\">'),
    '{w': ColorToken('', '[w', '{w', '&w', '~w', '%^WHITE%^', '\033[37m', '<COLOR FORE=\"#bbbbbb\">'),

    '{D': ColorToken('', '[D', '{D', '&z', '~z', '%^BOLD%^BLACK%^', '\033[1;30m', '<COLOR FORE=\"#555555\">'),
    '{R': ColorToken('', '[R', '{R', '&R', '~R', '%^BOLD%^RED%^', '\033[1;31m', '<COLOR FORE=\"#ff5555\">'),
    '{G': ColorToken('', '[G', '{G', '&G', '~G', '%^BOLD%^GREEN%^', '\033[1;32m', '<COLOR FORE=\"#55ff55\">'),
    '{Y': ColorToken('', '[Y', '{Y', '&Y', '~Y', '%^BOLD%^ORANGE%^', '\033[1;33m', '<COLOR FORE=\"#ffff55\">'),
    '{B': ColorToken('', '[B', '{B', '&B', '~B', '%^BOLD%^BLUE%^', '\033[1;34m', '<COLOR FORE=\"#5555ff\">'),
    '{M': ColorToken('', '[M', '{M', '&P', '~P', '%^BOLD%^MAGENTA%^', '\033[1;35m', '<COLOR FORE=\"#ff55ff\">'),
    '{C': ColorToken('', '[C', '{C', '&C', '~C', '%^BOLD%^CYAN%^', '\033[1;36m', '<COLOR FORE=\"#55ffff\">'),
    '{W': ColorToken('', '[W', '{W', '&W', '~W', '%^BOLD%^WHITE%^', '\033[1;37m', '<COLOR FORE=\"#ffffff\">'),

    '{*': ColorToken('', '[*', '{*', '', '', '', '\007', ''),
    '{/': ColorToken('', '[/', '{/', '', '', '', '\012', ''),

    '{{': ColorToken('{', '{', '{{', '{', '{', '{', '{', '{'),
    '}}': ColorToken('}', '}', '}}', '}}', '}', '}', '}', '}'),

    '{x': ColorToken('', '[x', '{x', '&d', '~!', '%^RESET%^', '\033[0m', '<RESET>'),
    '{L': ColorToken('', '[L', '{L', '&L', '~L', '%^BOLD%^', '\033[1m', '<BOLD>'),
    '{i': ColorToken('', '[i', '{i', '&i', '~i', '%^ITALIC%^', '\033[3m', '<ITALIC>'),
    '{u': ColorToken('', '[u', '{u', '&u', '~u', '%^UNDERLINE%^', '\033[4m', '<UNDERLINE>'),
    '{f': ColorToken('', '[f', '{f', '&f', '~$', '%^FLASH%^', '\033[5m', '<FONT COLOR=BLINK>'),
    '{V': ColorToken('', '[v', '{v', '&v', '~v', '%^REVERSE%^', '\033[7m', '<FONT COLOR=INVERSE>'),
    '{s': ColorToken('', '[s', '{s', '&s', '~s', '%^STRIKETHRU%^', '\033[9m', '<STRIKEOUT>'),

    '{H': ColorToken('', '[H', '{H', '', '', '%^HOME%^', '\033[H', ''),  # Home
    '{_': ColorToken('', '[_', '{_', '', '', '%^CLEARLINE%^', '\033[K', ''),  # Clear to end of line
    '{@': ColorToken('', '[@', '{@', '', '', '', '\033[J', ''),  # Clear to end of screen
    '{^': ColorToken('', '[^', '{^', '', '', '%^CURS_UP%^', '\033[A', ''),  # Cursor up
    '{v': ColorToken('', '[v', '{v', '', '', '%^CURS_DOWN%^', '\033[B', ''),  # Cursor down
    '{>': ColorToken('', '[>', '{>', '', '', '%^CURS_RIGHT%^', '\033[C', ''),  # Cursor right
    '{<': ColorToken('', '[<', '{<', '', '', '%^CURS_LEFT%^', '\033[D', ''),  # Cursor left

    # Background colors
    '}d': ColorToken('', ']d', '}d', '^x', '^x', '%^B_BLACK%^', '\033[40m', '<COLOR BACK=\"#000000\">'),
    '}r': ColorToken('', ']r', '}r', '^r', '^r', '%^B_RED%^', '\033[41m', '<COLOR BACK=\"#bb0000\">'),
    '}g': ColorToken('', ']g', '}g', '^g', '^g', '%^B_GREEN%^', '\033[42m', '<COLOR BACK=\"#00bb00\">'),
    '}y': ColorToken('', ']y', '}y', '^O', '^y', '%^B_ORANGE%^', '\033[43m', '<COLOR BACK=\"#bbbb00\">'),
    '}b': ColorToken('', ']b', '}b', '^b', '^b', '%^B_BLUE%^', '\033[44m', '<COLOR BACK=\"#0000bb\">'),
    '}m': ColorToken('', ']m', '}m', '^p', '^p', '%^B_MAGENTA%^', '\033[45m', '<COLOR BACK=\"#bb00bb\">'),
    '}c': ColorToken('', ']c', '}c', '^c', '^c', '%^B_CYAN%^', '\033[46m', '<COLOR BACK=\"#00bbbb\">'),
    '}w': ColorToken('', ']w', '}w', '^w', '^w', '%^B_WHITE%^', '\033[47m', '<COLOR BACK=\"#bbbbbb\">'),

    # Background colors cannot BE bold in ANSI
    '}D': ColorToken('', ']D', '}D', '^z', '^z', '%^B_BLACK%^', '\033[40m', '<COLOR BACK=\"#555555\">'),
    '}R': ColorToken('', ']R', '}R', '^R', '^R', '%^B_RED%^', '\033[41m', '<COLOR BACK=\"#ff5555\">'),
    '}G': ColorToken('', ']G', '}G', '^G', '^G', '%^B_GREEN%^', '\033[42m', '<COLOR BACK=\"#55ff55\">'),
    '}Y': ColorToken('', ']Y', '}Y', '^Y', '^Y', '%^B_ORANGE%^', '\033[43m', '<COLOR BACK=\"#ffff55\">'),
    '}B': ColorToken('', ']B', '}B', '^B', '^B', '%^B_BLUE%^', '\033[44m', '<COLOR BACK=\"#5555ff\">'),
    '}M': ColorToken('', ']M', '}M', '^P', '^P', '%^B_MAGENTA%^', '\033[45m', '<COLOR BACK=\"#ff55ff\">'),
    '}C': ColorToken('', ']C', '}C', '^C', '^C', '%^B_CYAN%^', '\033[46m', '<COLOR BACK=\"#55ffff\">'),
    '}W': ColorToken('', ']W', '}W', '^W', '^W', '%^B_WHITE%^', '\033[47m', '<COLOR BACK=\"#ffffff\">'),
}

COLOR_MAP['smaug'] = {
    '&x': ColorToken('', '[d', '{d', '&x', '~x', '%^BLACK%^', '\033[30m', '<COLOR FORE=\"#000000\">'),
    '&r': ColorToken('', '[r', '{r', '&r', '~r', '%^RED%^', '\033[31m', '<COLOR FORE=\"#bb0000\">'),
    '&g': ColorToken('', '[g', '{g', '&g', '~g', '%^GREEN%^', '\033[32m', '<COLOR FORE=\"#00bb00\">'),
    '&O': ColorToken('', '[y', '{y', '&O', '~y', '%^ORANGE%^', '\033[33m', '<COLOR FORE=\"#bbbb00\">'),
    '&b': ColorToken('', '[b', '{b', '&b', '~b', '%^BLUE%^', '\033[34m', '<COLOR FORE=\"#0000bb\">'),
    '&p': ColorToken('', '[m', '{m', '&p', '~p', '%^MAGENTA%^', '\033[35m', '<COLOR FORE=\"#bb00bb\">'),
    '&c': ColorToken('', '[c', '{c', '&c', '~c', '%^CYAN%^', '\033[36m', '<COLOR FORE=\"#00bbbb\">'),
    '&w': ColorToken('', '[w', '{w', '&w', '~w', '%^WHITE%^', '\033[37m', '<COLOR FORE=\"#bbbbbb\">'),

    '&z': ColorToken('', '[D', '{D', '&z', '~z', '%^BOLD%^BLACK%^', '\033[1;30m', '<COLOR FORE=\"#555555\">'),
    '&R': ColorToken('', '[R', '{R', '&R', '~R', '%^BOLD%^RED%^', '\033[1;31m', '<COLOR FORE=\"#ff5555\">'),
    '&G': ColorToken('', '[G', '{G', '&G', '~G', '%^BOLD%^GREEN%^', '\033[1;32m', '<COLOR FORE=\"#55ff55\">'),
    '&Y': ColorToken('', '[Y', '{Y', '&Y', '~Y', '%^BOLD%^ORANGE%^', '\033[1;33m', '<COLOR FORE=\"#ffff55\">'),
    '&B': ColorToken('', '[B', '{B', '&B', '~B', '%^BOLD%^BLUE%^', '\033[1;34m', '<COLOR FORE=\"#5555ff\">'),
    '&P': ColorToken('', '[M', '{M', '&P', '~P', '%^BOLD%^MAGENTA%^', '\033[1;35m', '<COLOR FORE=\"#ff55ff\">'),
    '&C': ColorToken('', '[C', '{C', '&C', '~C', '%^BOLD%^CYAN%^', '\033[1;36m', '<COLOR FORE=\"#55ffff\">'),
    '&W': ColorToken('', '[W', '{W', '&W', '~W', '%^BOLD%^WHITE%^', '\033[1;37m', '<COLOR FORE=\"#ffffff\">'),

    '&&': ColorToken('&', '&', '&', '&&', '&', '&', '&', '&'),
    '^^': ColorToken('^', '^', '^', '^^', '^^', '^', '^', '^'),
    '}}': ColorToken('}', '}', '}}', '}}', '}', '}', '}', '}'),

    '&d': ColorToken('', '[x', '{x', '&d', '~!', '%^RESET%^', '\033[0m', '<RESET>'),
    '&L': ColorToken('', '[L', '{L', '&L', '~L', '%^BOLD%^', '\033[1m', '<BOLD>'),
    '&i': ColorToken('', '[i', '{i', '&i', '~i', '%^ITALIC%^', '\033[3m', '<ITALIC>'),
    '&u': ColorToken('', '[u', '{u', '&u', '~u', '%^UNDERLINE%^', '\033[4m', '<UNDERLINE>'),
    '&f': ColorToken('', '[f', '{f', '&f', '~$', '%^FLASH%^', '\033[5m', '<FONT COLOR=BLINK>'),
    '&v': ColorToken('', '[v', '{v', '&v', '~v', '%^REVERSE%^', '\033[7m', '<FONT COLOR=INVERSE>'),
    '&s': ColorToken('', '[s', '{s', '&s', '~s', '%^STRIKETHRU%^', '\033[9m', '<STRIKEOUT>'),
    '&I': ColorToken('', '[i', '{i', '&i', '~i', '%^ITALIC%^', '\033[3m', '<ITALIC>'),
    '&U': ColorToken('', '[u', '{u', '&u', '~u', '%^UNDERLINE%^', '\033[4m', '<UNDERLINE>'),
    '&F': ColorToken('', '[f', '{f', '&f', '~$', '%^FLASH%^', '\033[5m', '<FONT COLOR=BLINK>'),
    '&V': ColorToken('', '[v', '{v', '&v', '~v', '%^REVERSE%^', '\033[7m', '<FONT COLOR=INVERSE>'),
    '&S': ColorToken('', '[s', '{s', '&s', '~s', '%^STRIKETHRU%^', '\033[9m', '<STRIKEOUT>'),

    # Background colors
    '^x': ColorToken('', ']d', '}d', '^x', '^x', '%^B_BLACK%^', '\033[40m', '<COLOR BACK=\"#000000\">'),
    '^r': ColorToken('', ']r', '}r', '^r', '^r', '%^B_RED%^', '\033[41m', '<COLOR BACK=\"#bb0000\">'),
    '^g': ColorToken('', ']g', '}g', '^g', '^g', '%^B_GREEN%^', '\033[42m', '<COLOR BACK=\"#00bb00\">'),
    '^O': ColorToken('', ']y', '}y', '^O', '^y', '%^B_ORANGE%^', '\033[43m', '<COLOR BACK=\"#bbbb00\">'),
    '^b': ColorToken('', ']b', '}b', '^b', '^b', '%^B_BLUE%^', '\033[44m', '<COLOR BACK=\"#0000bb\">'),
    '^p': ColorToken('', ']m', '}m', '^p', '^p', '%^B_MAGENTA%^', '\033[45m', '<COLOR BACK=\"#bb00bb\">'),
    '^c': ColorToken('', ']c', '}c', '^c', '^c', '%^B_CYAN%^', '\033[46m', '<COLOR BACK=\"#00bbbb\">'),
    '^w': ColorToken('', ']w', '}w', '^w', '^w', '%^B_WHITE%^', '\033[47m', '<COLOR BACK=\"#bbbbbb\">'),

    # Background colors cannot BE bold in ANSI
    '^z': ColorToken('', ']D', '}D', '^z', '^z', '%^B_BLACK%^', '\033[40m', '<COLOR BACK=\"#555555\">'),
    '^R': ColorToken('', ']R', '}R', '^R', '^R', '%^B_RED%^', '\033[41m', '<COLOR BACK=\"#ff5555\">'),
    '^G': ColorToken('', ']G', '}G', '^G', '^G', '%^B_GREEN%^', '\033[42m', '<COLOR BACK=\"#55ff55\">'),
    '^Y': ColorToken('', ']Y', '}Y', '^Y', '^Y', '%^B_ORANGE%^', '\033[43m', '<COLOR BACK=\"#ffff55\">'),
    '^B': ColorToken('', ']B', '}B', '^B', '^B', '%^B_BLUE%^', '\033[44m', '<COLOR BACK=\"#5555ff\">'),
    '^P': ColorToken('', ']M', '}M', '^P', '^P', '%^B_MAGENTA%^', '\033[45m', '<COLOR BACK=\"#ff55ff\">'),
    '^C': ColorToken('', ']C', '}C', '^C', '^C', '%^B_CYAN%^', '\033[46m', '<COLOR BACK=\"#55ffff\">'),
    '^W': ColorToken('', ']W', '}W', '^W', '^W', '%^B_WHITE%^', '\033[47m', '<COLOR BACK=\"#ffffff\">'),

    # Blinking colors
    '}x': ColorToken('', '[f[d', '{f{d', '}x', '`x', '%^FLASH%^BLACK%^', '\033[5;30m', '<FONT COLOR=BLINK><COLOR FORE=\"#000000\">'),
    '}r': ColorToken('', '[f[r', '{f{r', '}r', '`r', '%^FLASH%^RED%^', '\033[5;31m', '<FONT COLOR=BLINK><COLOR FORE=\"#bb0000\">'),
    '}g': ColorToken('', '[f[g', '{f{g', '}g', '`g', '%^FLASH%^GREEN%^', '\033[5;32m', '<FONT COLOR=BLINK><COLOR FORE=\"#00bb00\">'),
    '}O': ColorToken('', '[f[y', '{f{y', '}O', '`y', '%^FLASH%^ORANGE%^', '\033[5;33m', '<FONT COLOR=BLINK><COLOR FORE=\"#bbbb00\">'),
    '}b': ColorToken('', '[f[b', '{f{b', '}b', '`b', '%^FLASH%^BLUE%^', '\033[5;34m', '<FONT COLOR=BLINK><COLOR FORE=\"#0000bb\">'),
    '}p': ColorToken('', '[f[m', '{f{m', '}p', '`p', '%^FLASH%^MAGENTA%^', '\033[5;35m', '<FONT COLOR=BLINK><COLOR FORE=\"#bb00bb\">'),
    '}c': ColorToken('', '[f[c', '{f{c', '}c', '`c', '%^FLASH%^CYAN%^', '\033[5;36m', '<FONT COLOR=BLINK><COLOR FORE=\"#00bbbb\">'),
    '}w': ColorToken('', '[f[w', '{f{w', '}w', '`w', '%^FLASH%^WHITE%^', '\033[5;37m', '<FONT COLOR=BLINK><COLOR FORE=\"#bbbbbb\">'),

    '}z': ColorToken('', ']f]D', '{f{D', '}z', '`z', '%^FLASH%^BOLD%^BLACK%^', '\033[5;1;30m', '<FONT COLOR=BLINK><COLOR FORE=\"#555555\">'),
    '}R': ColorToken('', ']f]R', '{f{R', '}R', '`R', '%^FLASH%^BOLD%^RED%^', '\033[5;1;31m', '<FONT COLOR=BLINK><COLOR FORE=\"#ff5555\">'),
    '}G': ColorToken('', ']f]G', '{f{G', '}G', '`G', '%^FLASH%^BOLD%^GREEN%^', '\033[5;1;32m', '<FONT COLOR=BLINK><COLOR FORE=\"#55ff55\">'),
    '}Y': ColorToken('', ']f]Y', '{f{Y', '}Y', '`Y', '%^FLASH%^BOLD%^ORANGE%^', '\033[5;1;33m', '<FONT COLOR=BLINK><COLOR FORE=\"#ffff55\">'),
    '}B': ColorToken('', ']f]B', '{f{B', '}B', '`B', '%^FLASH%^BOLD%^BLUE%^', '\033[5;1;34m', '<FONT COLOR=BLINK><COLOR FORE=\"#5555ff\">'),
    '}P': ColorToken('', ']f]M', '{f{M', '}P', '`P', '%^FLASH%^BOLD%^MAGENTA%^', '\033[5;1;35m', '<FONT COLOR=BLINK><COLOR FORE=\"#ff55ff\">'),
    '}C': ColorToken('', ']f]C', '{f{C', '}C', '`C', '%^FLASH%^BOLD%^CYAN%^', '\033[5;1;36m', '<FONT COLOR=BLINK><COLOR FORE=\"#55ffff\">'),
    '}W': ColorToken('', ']f]W', '{f{W', '}W', '`W', '%^FLASH%^BOLD%^WHITE%^', '\033[5;1;37m', '<FONT COLOR=BLINK><COLOR FORE=\"#ffffff\">'),
}

COLOR_MAP['i3'] = {
    'BLACK':        ColorToken('', '[d', '{d', '&x', '~x', '%^BLACK%^', '\033[30m', '<COLOR FORE=\"#000000\">'),
    'RED':          ColorToken('', '[r', '{r', '&r', '~r', '%^RED%^', '\033[31m', '<COLOR FORE=\"#bb0000\">'),
    'GREEN':        ColorToken('', '[g', '{g', '&g', '~g', '%^GREEN%^', '\033[32m', '<COLOR FORE=\"#00bb00\">'),
    'ORANGE':       ColorToken('', '[y', '{y', '&O', '~y', '%^ORANGE%^', '\033[33m', '<COLOR FORE=\"#bbbb00\">'),
    'BLUE':         ColorToken('', '[b', '{b', '&b', '~b', '%^BLUE%^', '\033[34m', '<COLOR FORE=\"#0000bb\">'),
    'MAGENTA':      ColorToken('', '[m', '{m', '&p', '~p', '%^MAGENTA%^', '\033[35m', '<COLOR FORE=\"#bb00bb\">'),
    'CYAN':         ColorToken('', '[c', '{c', '&c', '~c', '%^CYAN%^', '\033[36m', '<COLOR FORE=\"#00bbbb\">'),
    'WHITE':        ColorToken('', '[w', '{w', '&w', '~w', '%^WHITE%^', '\033[37m', '<COLOR FORE=\"#bbbbbb\">'),

    'YELLOW':       ColorToken('', '[Y', '{Y', '&Y', '~Y', '%^BOLD%^ORANGE%^', '\033[1;33m', '<COLOR FORE=\"#ffff55\">'),

    'RESET':        ColorToken('', '[x', '{x', '&d', '~!', '%^RESET%^', '\033[0m', '<RESET>'),
    'BOLD':         ColorToken('', '[L', '{L', '&L', '~L', '%^BOLD%^', '\033[1m', '<BOLD>'),
    'ITALIC':       ColorToken('', '[i', '{i', '&i', '~i', '%^ITALIC%^', '\033[3m', '<ITALIC>'),
    'UNDERLINE':    ColorToken('', '[u', '{u', '&u', '~u', '%^UNDERLINE%^', '\033[4m', '<UNDERLINE>'),
    'FLASH':        ColorToken('', '[f', '{f', '&f', '~$', '%^FLASH%^', '\033[5m', '<FONT COLOR=BLINK>'),
    'REVERSE':      ColorToken('', '[v', '{v', '&v', '~v', '%^REVERSE%^', '\033[7m', '<FONT COLOR=INVERSE>'),
    'STRIKETHRU':   ColorToken('', '[s', '{s', '&s', '~s', '%^STRIKETHRU%^', '\033[9m', '<STRIKEOUT>'),

    'HOME':         ColorToken('', '[H', '{H', '', '', '%^HOME%^', '\033[H', ''),  # Home
    'CLEARLINE':    ColorToken('', '[_', '{_', '', '', '%^CLEARLINE%^', '\033[K', ''),  # Clear to end of line
    'CURS_UP':      ColorToken('', '[^', '{^', '', '', '%^CURS_UP%^', '\033[A', ''),  # Cursor up
    'CURS_DOWN':    ColorToken('', '[v', '{v', '', '', '%^CURS_DOWN%^', '\033[B', ''),  # Cursor down
    'CURS_RIGHT':   ColorToken('', '[>', '{>', '', '', '%^CURS_RIGHT%^', '\033[C', ''),  # Cursor right
    'CURS_LEFT':    ColorToken('', '[<', '{<', '', '', '%^CURS_LEFT%^', '\033[D', ''),  # Cursor left

    'B_BLACK':      ColorToken('', ']d', '}d', '^x', '^x', '%^B_BLACK%^', '\033[40m', '<COLOR BACK=\"#000000\">'),
    'B_RED':        ColorToken('', ']r', '}r', '^r', '^r', '%^B_RED%^', '\033[41m', '<COLOR BACK=\"#bb0000\">'),
    'B_GREEN':      ColorToken('', ']g', '}g', '^g', '^g', '%^B_GREEN%^', '\033[42m', '<COLOR BACK=\"#00bb00\">'),
    'B_ORANGE':     ColorToken('', ']y', '}y', '^O', '^y', '%^B_ORANGE%^', '\033[43m', '<COLOR BACK=\"#bbbb00\">'),
    'B_BLUE':       ColorToken('', ']b', '}b', '^b', '^b', '%^B_BLUE%^', '\033[44m', '<COLOR BACK=\"#0000bb\">'),
    'B_MAGENTA':    ColorToken('', ']m', '}m', '^p', '^p', '%^B_MAGENTA%^', '\033[45m', '<COLOR BACK=\"#bb00bb\">'),
    'B_CYAN':       ColorToken('', ']c', '}c', '^c', '^c', '%^B_CYAN%^', '\033[46m', '<COLOR BACK=\"#00bbbb\">'),
    'B_WHITE':      ColorToken('', ']w', '}w', '^w', '^w', '%^B_WHITE%^', '\033[47m', '<COLOR BACK=\"#bbbbbb\">'),

    'B_YELLOW':     ColorToken('', ']Y', '}Y', '^Y', '^Y', '%^B_ORANGE%^', '\033[43m', '<COLOR BACK=\"#ffff55\">'),
}

COLOR_MAP['imc2'] = {
    '~x': ColorToken('', '[d', '{d', '&x', '~x', '%^BLACK%^', '\033[30m', '<COLOR FORE=\"#000000\">'),
    '~r': ColorToken('', '[r', '{r', '&r', '~r', '%^RED%^', '\033[31m', '<COLOR FORE=\"#bb0000\">'),
    '~g': ColorToken('', '[g', '{g', '&g', '~g', '%^GREEN%^', '\033[32m', '<COLOR FORE=\"#00bb00\">'),
    '~y': ColorToken('', '[y', '{y', '&O', '~y', '%^ORANGE%^', '\033[33m', '<COLOR FORE=\"#bbbb00\">'),
    '~b': ColorToken('', '[b', '{b', '&b', '~b', '%^BLUE%^', '\033[34m', '<COLOR FORE=\"#0000bb\">'),
    '~p': ColorToken('', '[m', '{m', '&p', '~p', '%^MAGENTA%^', '\033[35m', '<COLOR FORE=\"#bb00bb\">'),
    '~c': ColorToken('', '[c', '{c', '&c', '~c', '%^CYAN%^', '\033[36m', '<COLOR FORE=\"#00bbbb\">'),
    '~w': ColorToken('', '[w', '{w', '&w', '~w', '%^WHITE%^', '\033[37m', '<COLOR FORE=\"#bbbbbb\">'),

    '~z': ColorToken('', '[D', '{D', '&z', '~z', '%^BOLD%^BLACK%^', '\033[1;30m', '<COLOR FORE=\"#555555\">'),
    '~R': ColorToken('', '[R', '{R', '&R', '~R', '%^BOLD%^RED%^', '\033[1;31m', '<COLOR FORE=\"#ff5555\">'),
    '~G': ColorToken('', '[G', '{G', '&G', '~G', '%^BOLD%^GREEN%^', '\033[1;32m', '<COLOR FORE=\"#55ff55\">'),
    '~Y': ColorToken('', '[Y', '{Y', '&Y', '~Y', '%^BOLD%^ORANGE%^', '\033[1;33m', '<COLOR FORE=\"#ffff55\">'),
    '~B': ColorToken('', '[B', '{B', '&B', '~B', '%^BOLD%^BLUE%^', '\033[1;34m', '<COLOR FORE=\"#5555ff\">'),
    '~P': ColorToken('', '[M', '{M', '&P', '~P', '%^BOLD%^MAGENTA%^', '\033[1;35m', '<COLOR FORE=\"#ff55ff\">'),
    '~C': ColorToken('', '[C', '{C', '&C', '~C', '%^BOLD%^CYAN%^', '\033[1;36m', '<COLOR FORE=\"#55ffff\">'),
    '~W': ColorToken('', '[W', '{W', '&W', '~W', '%^BOLD%^WHITE%^', '\033[1;37m', '<COLOR FORE=\"#ffffff\">'),

    '~~': ColorToken('~', '~', '~', '~', '~~', '~', '~', '~'),
    '^^': ColorToken('^', '^', '^', '^^', '^^', '^', '^', '^'),
    '``': ColorToken('`', '`', '`', '`', '``', '`', '`', '`'),

    '~!': ColorToken('', '[x', '{x', '&d', '~!', '%^RESET%^', '\033[0m', '<RESET>'),
    '~L': ColorToken('', '[L', '{L', '&L', '~L', '%^BOLD%^', '\033[1m', '<BOLD>'),
    '~i': ColorToken('', '[i', '{i', '&i', '~i', '%^ITALIC%^', '\033[3m', '<ITALIC>'),
    '~u': ColorToken('', '[u', '{u', '&u', '~u', '%^UNDERLINE%^', '\033[4m', '<UNDERLINE>'),
    '~$': ColorToken('', '[f', '{f', '&f', '~$', '%^FLASH%^', '\033[5m', '<FONT COLOR=BLINK>'),
    '~v': ColorToken('', '[v', '{v', '&v', '~v', '%^REVERSE%^', '\033[7m', '<FONT COLOR=INVERSE>'),
    '~s': ColorToken('', '[s', '{s', '&s', '~s', '%^STRIKETHRU%^', '\033[9m', '<STRIKEOUT>'),

    '~Z': ColorToken('', '', '', '&Z', '~Z', '', '', ''),  # Random foreground
    '~D': ColorToken('', '[D', '{D', '&z', '~z', '%^BOLD%^BLACK%^', '\033[1;30m', '<COLOR FORE=\"#555555\">'),
    '~m': ColorToken('', '[m', '{m', '&p', '~p', '%^MAGENTA%^', '\033[35m', '<COLOR FORE=\"#bb00bb\">'),
    '~d': ColorToken('', '[w', '{w', '&w', '~w', '%^WHITE%^', '\033[37m', '<COLOR FORE=\"#bbbbbb\">'),
    '~M': ColorToken('', '[M', '{M', '&P', '~P', '%^BOLD%^MAGENTA%^', '\033[1;35m', '<COLOR FORE=\"#ff55ff\">'),

    # Background colors
    '^x': ColorToken('', ']d', '}d', '^x', '^x', '%^B_BLACK%^', '\033[40m', '<COLOR BACK=\"#000000\">'),
    '^r': ColorToken('', ']r', '}r', '^r', '^r', '%^B_RED%^', '\033[41m', '<COLOR BACK=\"#bb0000\">'),
    '^g': ColorToken('', ']g', '}g', '^g', '^g', '%^B_GREEN%^', '\033[42m', '<COLOR BACK=\"#00bb00\">'),
    '^y': ColorToken('', ']y', '}y', '^O', '^y', '%^B_ORANGE%^', '\033[43m', '<COLOR BACK=\"#bbbb00\">'),
    '^b': ColorToken('', ']b', '}b', '^b', '^b', '%^B_BLUE%^', '\033[44m', '<COLOR BACK=\"#0000bb\">'),
    '^p': ColorToken('', ']m', '}m', '^p', '^p', '%^B_MAGENTA%^', '\033[45m', '<COLOR BACK=\"#bb00bb\">'),
    '^c': ColorToken('', ']c', '}c', '^c', '^c', '%^B_CYAN%^', '\033[46m', '<COLOR BACK=\"#00bbbb\">'),
    '^w': ColorToken('', ']w', '}w', '^w', '^w', '%^B_WHITE%^', '\033[47m', '<COLOR BACK=\"#bbbbbb\">'),

    # Background colors cannot BE bold in ANSI
    '^z': ColorToken('', ']D', '}D', '^z', '^z', '%^B_BLACK%^', '\033[40m', '<COLOR BACK=\"#555555\">'),
    '^R': ColorToken('', ']R', '}R', '^R', '^R', '%^B_RED%^', '\033[41m', '<COLOR BACK=\"#ff5555\">'),
    '^G': ColorToken('', ']G', '}G', '^G', '^G', '%^B_GREEN%^', '\033[42m', '<COLOR BACK=\"#55ff55\">'),
    '^Y': ColorToken('', ']Y', '}Y', '^Y', '^Y', '%^B_ORANGE%^', '\033[43m', '<COLOR BACK=\"#ffff55\">'),
    '^B': ColorToken('', ']B', '}B', '^B', '^B', '%^B_BLUE%^', '\033[44m', '<COLOR BACK=\"#5555ff\">'),
    '^P': ColorToken('', ']M', '}M', '^P', '^P', '%^B_MAGENTA%^', '\033[45m', '<COLOR BACK=\"#ff55ff\">'),
    '^C': ColorToken('', ']C', '}C', '^C', '^C', '%^B_CYAN%^', '\033[46m', '<COLOR BACK=\"#55ffff\">'),
    '^W': ColorToken('', ']W', '}W', '^W', '^W', '%^B_WHITE%^', '\033[47m', '<COLOR BACK=\"#ffffff\">'),

    '^D': ColorToken('', ']D', '}D', '^z', '^z', '%^B_BLACK%^', '\033[40m', '<COLOR BACK=\"#555555\">'),
    '^m': ColorToken('', ']m', '}m', '^p', '^p', '%^B_MAGENTA%^', '\033[45m', '<COLOR BACK=\"#bb00bb\">'),
    '^d': ColorToken('', ']w', '}w', '^w', '^w', '%^B_WHITE%^', '\033[47m', '<COLOR BACK=\"#bbbbbb\">'),
    '^M': ColorToken('', ']M', '}M', '^P', '^P', '%^B_MAGENTA%^', '\033[45m', '<COLOR BACK=\"#ff55ff\">'),

    # Blinking colors
    '`x': ColorToken('', '[f[d', '{f{d', '}x', '`x', '%^FLASH%^BLACK%^', '\033[5;30m', '<FONT COLOR=BLINK><COLOR FORE=\"#000000\">'),
    '`r': ColorToken('', '[f[r', '{f{r', '}r', '`r', '%^FLASH%^RED%^', '\033[5;31m', '<FONT COLOR=BLINK><COLOR FORE=\"#bb0000\">'),
    '`g': ColorToken('', '[f[g', '{f{g', '}g', '`g', '%^FLASH%^GREEN%^', '\033[5;32m', '<FONT COLOR=BLINK><COLOR FORE=\"#00bb00\">'),
    '`y': ColorToken('', '[f[y', '{f{y', '}O', '`y', '%^FLASH%^ORANGE%^', '\033[5;33m', '<FONT COLOR=BLINK><COLOR FORE=\"#bbbb00\">'),
    '`b': ColorToken('', '[f[b', '{f{b', '}b', '`b', '%^FLASH%^BLUE%^', '\033[5;34m', '<FONT COLOR=BLINK><COLOR FORE=\"#0000bb\">'),
    '`p': ColorToken('', '[f[m', '{f{m', '}p', '`p', '%^FLASH%^MAGENTA%^', '\033[5;35m', '<FONT COLOR=BLINK><COLOR FORE=\"#bb00bb\">'),
    '`c': ColorToken('', '[f[c', '{f{c', '}c', '`c', '%^FLASH%^CYAN%^', '\033[5;36m', '<FONT COLOR=BLINK><COLOR FORE=\"#00bbbb\">'),
    '`w': ColorToken('', '[f[w', '{f{w', '}w', '`w', '%^FLASH%^WHITE%^', '\033[5;37m', '<FONT COLOR=BLINK><COLOR FORE=\"#bbbbbb\">'),

    '`z': ColorToken('', '[f[D', '{f{D', '}z', '`z', '%^FLASH%^BOLD%^BLACK%^', '\033[5;1;30m', '<FONT COLOR=BLINK><COLOR FORE=\"#555555\">'),
    '`R': ColorToken('', '[f[R', '{f{R', '}R', '`R', '%^FLASH%^BOLD%^RED%^', '\033[5;1;31m', '<FONT COLOR=BLINK><COLOR FORE=\"#ff5555\">'),
    '`G': ColorToken('', '[f[G', '{f{G', '}G', '`G', '%^FLASH%^BOLD%^GREEN%^', '\033[5;1;32m', '<FONT COLOR=BLINK><COLOR FORE=\"#55ff55\">'),
    '`Y': ColorToken('', '[f[Y', '{f{Y', '}Y', '`Y', '%^FLASH%^BOLD%^ORANGE%^', '\033[5;1;33m', '<FONT COLOR=BLINK><COLOR FORE=\"#ffff55\">'),
    '`B': ColorToken('', '[f[B', '{f{B', '}B', '`B', '%^FLASH%^BOLD%^BLUE%^', '\033[5;1;34m', '<FONT COLOR=BLINK><COLOR FORE=\"#5555ff\">'),
    '`P': ColorToken('', '[f[M', '{f{M', '}P', '`P', '%^FLASH%^BOLD%^MAGENTA%^', '\033[5;1;35m', '<FONT COLOR=BLINK><COLOR FORE=\"#ff55ff\">'),
    '`C': ColorToken('', '[f[C', '{f{C', '}C', '`C', '%^FLASH%^BOLD%^CYAN%^', '\033[5;1;36m', '<FONT COLOR=BLINK><COLOR FORE=\"#55ffff\">'),
    '`W': ColorToken('', '[f[W', '{f{W', '}W', '`W', '%^FLASH%^BOLD%^WHITE%^', '\033[5;1;37m', '<FONT COLOR=BLINK><COLOR FORE=\"#ffffff\">'),

    '`D': ColorToken('', '[f[D', '{f{D', '}z', '`z', '%^FLASH%^BOLD%^B_BLACK%^', '\033[5;1;30m', '<FONT COLOR=BLINK><COLOR FORE=\"#555555\">'),
    '`m': ColorToken('', '[f[m', '{f{m', '}p', '`p', '%^FLASH%^MAGENTA%^', '\033[5;35m', '<FONT COLOR=BLINK><COLOR FORE=\"#bb00bb\">'),
    '`d': ColorToken('', '[f[w', '{f{w', '}w', '`w', '%^FLASH%^WHITE%^', '\033[5;37m', '<FONT COLOR=BLINK><COLOR FORE=\"#bbbbbb\">'),
    '`M': ColorToken('', '[f[M', '{f{M', '}P', '`P', '%^FLASH%^BOLD%^MAGENTA%^', '\033[5;1;35m', '<FONT COLOR=BLINK><COLOR FORE=\"#ff55ff\">'),
}
