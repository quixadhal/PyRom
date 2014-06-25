"""
 #**************************************************************************
 *  Original Diku Mud copyright=C) 1990, 1991 by Sebastian Hammer,         *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright=C) 1992, 1993 by Michael           *
 *  Chastain, Michael Quan, and Mitchell Tse.                              *
 *                                                                         *
 *  In order to use any part of this Merc Diku Mud, you must comply with   *
 *  both the original Diku license in 'license.doc' as well the Merc       *
 *  license in 'license.txt'.  In particular, you may not remove either of *
 *  these copyright notices.                                               *
 *                                                                         *
 *  Much time and thought has gone into this software and you are          *
 *  benefitting.  We hope that you share your changes too.  What goes      *
 *  around, comes around.                                                  *
 ***************************************************************************/

#**************************************************************************
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor=rtaylor@hypercube.org)                                 *
*       Gabrielle Taylor=gtaylor@hypercube.org)                            *
*       Brian Moore=zump@rom.org)                                          *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
#***********
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/
 ************/
 """
__author__ = 'syn'
import sys
import functools
import inspect
"""So far this wrapper class will allow debugging of a function as such:
@logger("Debug")
def some_func(stuff)

Once attached, it will safely try the function and print a failure.
It will also send a message to the calling character about a failure,
if there was a calling character.

Will add actual logfile support soon, and build out additional logging templates"""

def value_to_str(v):
    if isinstance(v, str):
        return ''.join(["'", v.replace('\n', '\\n'), "'"])
    else:
        # noinspection PyBroadException
        try:
            return str(v).replace('\n', '\\n')
        except:
            return '<ERROR: CANNOT PRINT>'

def parse_exception(error_object, *args):
    if hasattr(args[0][0], 'pcdata'):
        ch = args[0][0]
        ch.send("\nAn error has occurred. Sorry.\n")
    wrap_call = inspect.getinnerframes(sys.exc_info()[2])
    print("Exception: %s %s" % (type(error_object), str(error_object)))
    for call_info in reversed(wrap_call):
        local_calls = call_info[0].f_locals
        if '_logger__tracer_var_' in local_calls:
            continue
        print("Frame Trace - File: ", call_info[1],
              "Line: ", call_info[2],
              "Function: ", call_info[3],
              "Offending Code: ", call_info[4][0].lstrip())
        print("Local Env Variables: ")
        for k, v in local_calls.items():
            print("%s : %s " % (k, value_to_str(v)))


class logger(object):
    def __init__(self, log_type):
        """Init the logger, log_type"""
        self.log_type = log_type

    def __call__(self, func):
        """the class needs to be callable for this to work"""
        functools.update_wrapper(self, func)
    #Add debug log for any function you wish for TS, provides trace of incident
        if self.log_type == "Debug":
            def debug(*args, **kwargs):
                """__tracer_var_ becomes _logger__tracer_var_ in the trace.
                This is used to determine if we are within the wrapping frame
                or the wrapped frame.

                Leave this in place to receive only the wrapped frame trace info
                 - we dont care about the wrapping frame information."""
                __tracer_var_ = 0
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    parse_exception(err, args)
                    return
            return debug



