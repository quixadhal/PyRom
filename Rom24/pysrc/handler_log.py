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
import logging

logger = logging.getLogger()

import merc
import handler_pc

"""So far this wrapper class will allow debugging of a function as such:
@logger("Debug")
def some_func(stuff)

Once attached, it will safely try the function and print a failure.
It will also send a message to the calling character about a failure,
if there was a calling character.

Will add actual logfile support soon, and build out additional logging templates"""


class GlobalDebugFlag:
    """Enable or disable our global flags"""
    def gdfset(state):
        merc.GDF = state
        return

    def gdcfset(state):
        merc.GDCF = state
        return

def value_to_str(v):
    import interp
    if isinstance(v, handler_pc.Pc):
        return v.name
    elif isinstance(v, interp.cmd_type):
        return v.do_fun
    elif isinstance(v, str):
        return ''.join(["'", v.replace('\n', '\\n'), "'"])
    else:
        # noinspection PyBroadException
        try:
            return str(v).replace('\n', '\\n')
        except:
            return '<ERROR: CANNOT PRINT>'


def char_parse_exception(error_object, *args, ch):  # Parser for exceptions with a CH entity for extra msging
    merc.GDF = False
    wrap_call = inspect.getinnerframes(sys.exc_info()[2])
    if ch.level == merc.ML:
        ch.send("An Exception Occurred: \n%s %s\n\n" % (type(error_object), str(error_object)))
    logger.debug("Exception: %s %s" % (type(error_object), str(error_object)))
    for call_info in reversed(wrap_call):
        local_calls = call_info[0].f_locals
        if '_logged__tracer_var_' in local_calls:
            continue
        if ch.level == merc.ML:
            ch.send("--Frame Trace-- \nFile: %s \nFunction: %s \nLine: %d \nCode: %s "
                    % (call_info[1], call_info[3], call_info[2], call_info[4][0].lstrip()))
            ch.send("\n")
        logger.debug("--Frame Trace-- \nFile: %s \nFunction: %s \nLine: %d \nCode: %s "
                     % (call_info[1], call_info[3], call_info[2], call_info[4][0].lstrip()))
        logger.debug("Local Env Variables: ")
        for k, v in local_calls.items():
            levtrace = value_to_str(v)
            logger.debug("%s : %s", k, levtrace)


def noch_parse_exception(error_object, *args):
    merc.GDF = False
    wrap_call = inspect.getinnerframes(sys.exc_info()[2])
    logger.debug("Exception: %s %s" % (type(error_object), str(error_object)))
    for call_info in reversed(wrap_call):
        local_calls = call_info[0].f_locals
        if '_logged__tracer_var_' in local_calls:
            continue
        tracestring = "Frame Trace: \nFile: %s \nLine: %d \n ", call_info[1], call_info[2]
        tracestring += "Function: %s \nCode: %s ", call_info[3], call_info[4][0].lstrip()
        logger.debug(tracestring)
        logger.debug("Local Env Variables: ")
        for k, v in local_calls.items():
            levtrace = value_to_str(v)
            logger.debug("%s : %s", k, levtrace)


class logged(object):
    def __init__(self, log_type, ch=None):
        """Init the logger, log_type"""
        self.log_type = log_type
        self.ch = ch

    def __call__(self, func):
        """the class needs to be callable for this to work"""
        functools.update_wrapper(self, func)

    #Add debug log for any function you wish for TS, provides trace of incident
        if self.log_type == "Debug":  # Used to wrap any function and does not know about or care about flags
            def debug(*args, **kwargs):
                if args and isinstance(args[0], handler_pc.Pc):
                    mch = args[0]
                else:
                    mch = self.ch
                """__tracer_var_ becomes _logger__tracer_var_ in the trace.
                This is used to determine if we are within the wrapping frame
                or the wrapped frame.

                Leave this in place to receive only the wrapped frame trace info
                 - we dont care about the wrapping frame information."""
                __tracer_var_ = 0
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    if isinstance(mch, handler_pc.Pc):
                        if mch.level == merc.ML:
                            mch.send("Debug has been Enabled\n\n")
                        char_parse_exception(err, args, ch=mch)
                    else:
                        noch_parse_exception(err, args)
                    return
            return debug

        if self.log_type == "Interp":  # Used with interp and either debug command, or global debug flag
            def interp_debug(*args, **kwargs):
                if merc.GDF is False and merc.GDCF is False:  # Check for global/debug command flags
                    return func(*args, **kwargs)  # if none of the debugs are on, just send the command as normal
                if args and isinstance(args[0], handler_pc.Pc):
                    """check if there are args, and the args entail a character structure"""
                    mch = args[0]  # If so, lets make a char object so we can send messages as needed
                else:
                    mch = self.ch  # If so, lets make a char object so we can send messages as needed
                """__tracer_var_ becomes _logger__tracer_var_ in the trace.
                This is used to determine if we are within the wrapping frame
                or the wrapped frame.

                Leave this in place to receive only the wrapped frame trace info
                 - we dont care about the wrapping frame information."""
                __tracer_var_ = 0
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    if isinstance(mch, handler_pc.Pc):
                        mch.send("Debug has been Enabled\n\n")
                        char_parse_exception(err, args, ch=mch)
                    else:
                        noch_parse_exception(err, args)
                    return
            return interp_debug

        else:
            return func



