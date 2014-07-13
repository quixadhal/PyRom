import logging

logger = logging.getLogger()

import merc
import const
import interp


def do_groups(ch, argument):
    if ch.is_npc():
        return
    col = 0

    if not argument:
        # show all groups
        for gn, group in const.group_table.items():
            if gn in ch.group_known:
                ch.send("%-20s " % group.name)
                col += 1
                if col % 3 == 0:
                    ch.send("\n")
        if col % 3 != 0:
            ch.send("\n")
        ch.send("Creation points: %d\n" % ch.points)
        return

    if "all" == argument.lower():
        for gn, group in const.group_table.items():
            ch.send("%-20s " % group.name)
            col += 1
            if col % 3 == 0:
                ch.send("\n")
        if col % 3 != 0:
            ch.send("\n")
        return

    # show the sub-members of a group
    if argument.lower() not in const.group_table:
        ch.send("No group of that name exist.\n")
        ch.send("Type 'groups all' or 'info all' for a full listing.\n")
        return

    gn = const.group_table[argument.lower()]
    for sn in gn.spells:  # TODO:  This might be incorrect.
        if not sn:
            break
        ch.send("%-20s " % sn)
        col += 1
        if col % 3 == 0:
            ch.send("\n")
    if col % 3 != 0:
        ch.send("\n")


interp.register_command(interp.cmd_type('info', do_groups, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type('groups', do_groups, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
