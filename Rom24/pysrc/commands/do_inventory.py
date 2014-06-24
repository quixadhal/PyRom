import merc
import interp


def do_inventory(ch, argument):
    ch.send("You are carrying:\n")
    merc.show_list_to_char(ch.carrying, ch, True, True)
    return

interp.cmd_table['inventory'] = interp.cmd_type('inventory', do_inventory, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)