import merc
import interp


def do_rset(ch, argument):
    argument, arg1  = merc.read_word(argument)
    argument, arg2  = merc.read_word(argument)
    arg3 = argument

    if not arg1 or not arg2 or not arg3:
        ch.send("Syntax:\n")
        ch.send("  set room <location> <field> <value>\n")
        ch.send("  Field being one of:\n")
        ch.send("    flags sector\n")
        return
    location = merc.find_location(ch, arg1)
    if not location:
        ch.send("No such location.\n")
        return
    if not ch.is_room_owner(location) and ch.in_room != location \
    and location.is_private() and not merc.IS_TRUSTED(ch, merc.IMPLEMENTOR):
        ch.send("That room is private right now.\n")
        return

    #* Snarf the value.
    if not arg3.isdigit():
        ch.send("Value must be numeric.\n")
        return
    value = int(arg3)

    #* Set something.
    if "flags".startswith(arg2):
        location.room_flags  = value
        return
    if "sector".startswith(arg2):
        location.sector_type = value
        return
    #  Generate usage message.
    ch.do_rset("")
    return

interp.cmd_table['rset'] = interp.cmd_type('rset', do_rset, merc.POS_DEAD, merc.L2, merc.LOG_ALWAYS, 1)