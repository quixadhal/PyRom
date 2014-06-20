# -*- coding: utf-8 -*- line endings: unix -*-
#------------------------------------------------------------------------------
#   miniboa/colors.py
#   Copyright 2009 Jim Storch
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain a
#   copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
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
#------------------------------------------------------------------------------
"""
Split off the color codes themselves into a seperate module
to make it easier to edit the actual terminal code
"""

_TERMINAL_TYPES = ['unknown', 'ansi', 'imc2', 'i3', 'mxp']
_COLOR_TOKENS = ['BOLD', 'FLASH', 'ITALIC', 'RESET', 'REVERSE', 'STRIKETHRU', 'UNDERLINE',
    'CLEARLINE', 'CURS_DOWN', 'CURS_LEFT', 'CURS_RIGHT', 'CURS_UP',
    'ENDTERM', 'HOME', 'INITTERM', 'RESTORE', 'SAVE',
    'BLACK', 'RED', 'GREEN', 'ORANGE',
    'BLUE', 'MAGENTA', 'CYAN', 'GREY',
    'DARKGREY', 'LIGHTRED', 'LIGHTGREEN', 'YELLOW',
    'LIGHTBLUE', 'PINK', 'LIGHTCYAN', 'WHITE',
    'B_BLACK', 'B_RED', 'B_GREEN', 'B_ORANGE',
    'B_BLUE', 'B_MAGENTA', 'B_CYAN', 'B_GREY',
    'B_DARKGREY', 'B_LIGHTRED', 'B_LIGHTGREEN', 'B_YELLOW',
    'B_LIGHTBLUE', 'B_PINK', 'B_LIGHTCYAN', 'B_WHITE']

_COLOR_MAP = {}

for k in _TERMINAL_TYPES:
    _COLOR_MAP[k] = {}

for k in _COLOR_TOKENS:
    _COLOR_MAP['unknown'][k] = ''

_COLOR_MAP['ansi'] = {
    'BOLD'              : "\033[1m",
    'FLASH'             : "\033[5m",
    'ITALIC'            : "\033[3m",
    'RESET'             : "\033[0m",
    'REVERSE'           : "\033[7m",
    'STRIKETHRU'        : "\033[9m",
    'UNDERLINE'         : "\033[4m",

    'CLEARLINE'         : "\033[L\033[G",
    'CURS_DOWN'         : "\033[B",
    'CURS_LEFT'         : "\033[D",
    'CURS_RIGHT'        : "\033[C",
    'CURS_UP'           : "\033[A",

    'ENDTERM'           : "",
    'HOME'              : "\033[H",
    'INITTERM'          : "\033[H\033[2J",
    'RESTORE'           : "\033[u",
    'SAVE'              : "\033[s",

    'BLACK'             : "\033[30m",
    'RED'               : "\033[31m",
    'GREEN'             : "\033[32m",
    'ORANGE'            : "\033[33m",
    'BLUE'              : "\033[34m",
    'MAGENTA'           : "\033[35m",
    'CYAN'              : "\033[36m",
    'GREY'              : "\033[37m",

    'DARKGREY'          : "\033[1;30m",
    'LIGHTRED'          : "\033[1;31m",
    'LIGHTGREEN'        : "\033[1;32m",
    'YELLOW'            : "\033[1;33m",
    'LIGHTBLUE'         : "\033[1;34m",
    'PINK'              : "\033[1;35m",
    'LIGHTCYAN'         : "\033[1;36m",
    'WHITE'             : "\033[1;37m",

    'B_BLACK'           : "\033[40m",
    'B_RED'             : "\033[41m",
    'B_GREEN'           : "\033[42m",
    'B_ORANGE'          : "\033[43m",
    'B_BLUE'            : "\033[44m",
    'B_MAGENTA'         : "\033[45m",
    'B_CYAN'            : "\033[46m",
    'B_GREY'            : "\033[47m",

    'B_DARKGREY'        : "\033[40m",
    'B_LIGHTRED'        : "\033[41m",
    'B_LIGHTGREEN'      : "\033[42m",
    'B_YELLOW'          : "\033[43m",
    'B_LIGHTBLUE'       : "\033[44m",
    'B_PINK'            : "\033[45m",
    'B_LIGHTCYAN'       : "\033[46m",
    'B_WHITE'           : "\033[47m"
    }

_COLOR_MAP['imc2'] = {
    'BOLD'              : "~L",
    'FLASH'             : "~\$",
    'ITALIC'            : "~i",
    'RESET'             : "~!",
    'REVERSE'           : "~v",
    'STRIKETHRU'        : "~s",
    'UNDERLINE'         : "~u",

    'CLEARLINE'         : "",
    'CURS_DOWN'         : "",
    'CURS_LEFT'         : "",
    'CURS_RIGHT'        : "",
    'CURS_UP'           : "",

    'ENDTERM'           : "",
    'HOME'              : "",
    'INITTERM'          : "",
    'RESTORE'           : "",
    'SAVE'              : "",

    'BLACK'             : "~x",
    'RED'               : "~r",
    'GREEN'             : "~g",
    'ORANGE'            : "~y",
    'BLUE'              : "~b",
    'MAGENTA'           : "~p",
    'CYAN'              : "~c",
    'GREY'              : "~w",

    'DARKGREY'          : "~z",
    'LIGHTRED'          : "~R",
    'LIGHTGREEN'        : "~G",
    'YELLOW'            : "~Y",
    'LIGHTBLUE'         : "~B",
    'PINK'              : "~P",
    'LIGHTCYAN'         : "~C",
    'WHITE'             : "~W",

    'B_BLACK'           : "^x",
    'B_RED'             : "^r",
    'B_GREEN'           : "^g",
    'B_ORANGE'          : "^O",
    'B_BLUE'            : "^b",
    'B_MAGENTA'         : "^p",
    'B_CYAN'            : "^c",
    'B_GREY'            : "^w",

    'B_DARKGREY'        : "^z",
    'B_LIGHTRED'        : "^R",
    'B_LIGHTGREEN'      : "^G",
    'B_YELLOW'          : "^Y",
    'B_LIGHTBLUE'       : "^B",
    'B_PINK'            : "^P",
    'B_LIGHTCYAN'       : "^C",
    'B_WHITE'           : "^W",
    }

_COLOR_MAP['i3'] = {
    'BOLD'              : "%^BOLD%^",
    'FLASH'             : "%^FLASH%^",
    'ITALIC'            : "%^ITALIC%^",
    'RESET'             : "%^RESET%^",
    'REVERSE'           : "%^REVERSE%^",
    'STRIKETHRU'        : "%^STRIKETHRU%^",
    'UNDERLINE'         : "%^UNDERLINE%^",

    'CLEARLINE'         : "%^CLEARLINE%^",
    'CURS_DOWN'         : "%^CURS_DOWN%^",
    'CURS_LEFT'         : "%^CURS_LEFT%^",
    'CURS_RIGHT'        : "%^CURS_RIGHT%^",
    'CURS_UP'           : "%^CURS_UP%^",

    'ENDTERM'           : "%^ENDTERM%^",
    'HOME'              : "%^HOME%^",
    'INITTERM'          : "%^INITTERM%^",
    'RESTORE'           : "%^RESTORE%^",
    'SAVE'              : "%^SAVE%^",

    'BLACK'             : "%^BLACK%^",
    'RED'               : "%^RED%^",
    'GREEN'             : "%^GREEN%^",
    'ORANGE'            : "%^ORANGE%^",
    'BLUE'              : "%^BLUE%^",
    'MAGENTA'           : "%^MAGENTA%^",
    'CYAN'              : "%^CYAN%^",
    'GREY'              : "%^WHITE%^",

    'DARKGREY'          : "%^BOLD%^BLACK%^",
    'LIGHTRED'          : "%^BOLD%^RED%^",
    'LIGHTGREEN'        : "%^BOLD%^GREEN%^",
    'YELLOW'            : "%^YELLOW%^",
    'LIGHTBLUE'         : "%^BOLD%^BLUE%^",
    'PINK'              : "%^BOLD%^MAGENTA%^",
    'LIGHTCYAN'         : "%^BOLD%^CYAN%^",
    'WHITE'             : "%^BOLD%^WHITE%^",

    'B_BLACK'           : "%^B_BLACK%^",
    'B_RED'             : "%^B_RED%^",
    'B_GREEN'           : "%^B_GREEN%^",
    'B_ORANGE'          : "%^B_ORANGE%^",
    'B_BLUE'            : "%^B_BLUE%^",
    'B_MAGENTA'         : "%^B_MAGENTA%^",
    'B_CYAN'            : "%^B_CYAN%^",
    'B_GREY'            : "%^B_WHITE%^",

    'B_DARKGREY'        : "%^B_BLACK%^",
    'B_LIGHTRED'        : "%^B_RED%^",
    'B_LIGHTGREEN'      : "%^B_GREEN%^",
    'B_YELLOW'          : "%^B_YELLOW%^",
    'B_LIGHTBLUE'       : "%^B_BLUE%^",
    'B_PINK'            : "%^B_MAGENTA%^",
    'B_LIGHTCYAN'       : "%^B_CYAN%^",
    'B_WHITE'           : "%^B_WHITE%^",
    }

_COLOR_MAP['mxp'] = {
    'BOLD'              : "<BOLD>",
    'FLASH'             : "<FONT COLOR=BLINK>",
    'ITALIC'            : "<ITALIC>",
    'RESET'             : "<RESET>",
    'REVERSE'           : "<FONT COLOR=INVERSE>",
    'STRIKETHRU'        : "<STRIKEOUT>",
    'UNDERLINE'         : "<UNDERLINE>",

    'CLEARLINE'         : "",
    'CURS_DOWN'         : "",
    'CURS_LEFT'         : "",
    'CURS_RIGHT'        : "",
    'CURS_UP'           : "",

    'ENDTERM'           : "",
    'HOME'              : "",
    'INITTERM'          : "",
    'RESTORE'           : "",
    'SAVE'              : "",

    'BLACK'             : "<COLOR FORE=\"#000000\">",
    'RED'               : "<COLOR FORE=\"#bb0000\">",
    'GREEN'             : "<COLOR FORE=\"#00bb00\">",
    'ORANGE'            : "<COLOR FORE=\"#bbbb00\">",
    'BLUE'              : "<COLOR FORE=\"#0000bb\">",
    'MAGENTA'           : "<COLOR FORE=\"#bb00bb\">",
    'CYAN'              : "<COLOR FORE=\"#00bbbb\">",
    'GREY'              : "<COLOR FORE=\"#bbbbbb\">",

    'DARKGREY'          : "<COLOR FORE=\"#555555\">",
    'LIGHTRED'          : "<COLOR FORE=\"#ff5555\">",
    'LIGHTGREEN'        : "<COLOR FORE=\"#55ff55\">",
    'YELLOW'            : "<COLOR FORE=\"#ffff55\">",
    'LIGHTBLUE'         : "<COLOR FORE=\"#5555ff\">",
    'PINK'              : "<COLOR FORE=\"#ff55ff\">",
    'LIGHTCYAN'         : "<COLOR FORE=\"#55ffff\">",
    'WHITE'             : "<COLOR FORE=\"#ffffff\">",

    'B_BLACK'           : "<COLOR BACK=\"#000000\">",
    'B_RED'             : "<COLOR BACK=\"#bb0000\">",
    'B_GREEN'           : "<COLOR BACK=\"#00bb00\">",
    'B_ORANGE'          : "<COLOR BACK=\"#bbbb00\">",
    'B_BLUE'            : "<COLOR BACK=\"#0000bb\">",
    'B_MAGENTA'         : "<COLOR BACK=\"#bb00bb\">",
    'B_CYAN'            : "<COLOR BACK=\"#00bbbb\">",
    'B_GREY'            : "<COLOR BACK=\"#bbbbbb\">",
                                                      
    'B_DARKGREY'        : "<COLOR BACK=\"#555555\">",
    'B_LIGHTRED'        : "<COLOR BACK=\"#ff5555\">",
    'B_LIGHTGREEN'      : "<COLOR BACK=\"#55ff55\">",
    'B_YELLOW'          : "<COLOR BACK=\"#ffff55\">",
    'B_LIGHTBLUE'       : "<COLOR BACK=\"#5555ff\">",
    'B_PINK'            : "<COLOR BACK=\"#ff55ff\">",
    'B_LIGHTCYAN'       : "<COLOR BACK=\"#55ffff\">",
    'B_WHITE'           : "<COLOR BACK=\"#ffffff\">",
    }

