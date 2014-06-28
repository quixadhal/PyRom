import logging

logger = logging.getLogger()

import merc
import interp
import game_utils


# ofind and mfind replaced with vnum, vnum skill also added */
def do_vnum(ch, argument):
    string, arg = game_utils.read_word(argument)

    if not arg:
        ch.send("Syntax:\n")
        ch.send("  vnum obj <name>\n")
        ch.send("  vnum mob <name>\n")
        ch.send("  vnum skill <skill or spell>\n")
        return
    if arg == "obj":
        ch.do_ofind(string)
        return

    if arg == "mob" or arg == "char":
        ch.do_mfind(string)
        return

    if arg == "skill" or arg == "spell":
        ch.do_slookup(string)
        return
    # do both */
    ch.do_mfind(argument)
    ch.do_ofind(argument)


interp.register_command(interp.cmd_type('vnum', do_vnum, merc.POS_DEAD, merc.L4, merc.LOG_NORMAL, 1))
