import merc
import interp


# RT set replaces sset, mset, oset, and rset */
def do_set(ch, argument):
    argument, arg = merc.read_word(argument)

    if not arg:
        ch.send("Syntax:\n")
        ch.send("  set mob   <name> <field> <value>\n")
        ch.send("  set obj   <name> <field> <value>\n")
        ch.send("  set room  <room> <field> <value>\n")
        ch.send("  set skill <name> <spell or skill> <value>\n")
        return
    if "character".startswith(arg) or "mobile".startswith(arg):
        ch.do_mset(argument)
        return
    if "spell".startswith(arg) or "skill".startswith(arg):
        ch.do_sset(argument)
        return
    if "object".startswith(arg):
        ch.do_oset(argument)
        return
    if "room".startswith(arg):
        ch.do_rset(argument)
        return
    # echo syntax */
    ch.do_set("")

interp.cmd_table['set'] = interp.cmd_type('set', do_set, merc.POS_DEAD, merc.L2, merc.LOG_ALWAYS, 1)