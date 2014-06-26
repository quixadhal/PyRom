import merc
import interp


# RT to replace the two load commands */
def do_load(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Syntax:\n")
        ch.send("  load mob <vnum>\n")
        ch.send("  load obj <vnum> <level>\n")
        return
    if arg == "mob" or arg == "char":
        ch.do_mload(argument)
        return
    if arg == "obj":
        ch.do_oload(argument)
        return
    # echo syntax */
    ch.do_load("")

interp.cmd_table['load'] = interp.cmd_type('load', do_load, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1)