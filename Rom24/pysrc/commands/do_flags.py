import logging

logger = logging.getLogger()

import interp
import merc
import game_utils
import tables

__author__ = 'venom'

#int flag_lookup args( ( const char *name, const struct flag_type *flag_table) );


def do_flags(ch, argument):
    fadd = None
    frem = None
    fequals = None

    if '+' in argument:
        argument.strip('+')
        fadd = True
    elif '-' in argument:
        argument.strip('-')
        frem = True
    elif '=' in argument:
        argument.strip('=')
        fequals = True

    victim = None
    
    f_argument, arg1 = game_utils.read_word(argument)
    f_argument, arg2 = game_utils.read_word(f_argument)
    f_argument, arg3 = game_utils.read_word(f_argument)

    in_flags = set({})

    while f_argument:
        f_argument, aflag = game_utils.read_word(f_argument)
        in_flags |= set(aflag)

    if not argument:
        ch.send("Syntax:\n")
        ch.send("  flag mob  <name> <field> <flags>\n")
        ch.send("  flag char <name> <field> <flags>\n")
        ch.send("  mob  flags: act,aff,off,imm,res,vuln,form,part\n")
        ch.send("  char flags: plr,comm,aff,imm,res,vuln,\n")
        ch.send("  +: add flag, -: remove flag, = set equal to\n")
        ch.send("  otherwise flag toggles the flags listed.\n")
        return

    if not arg2:
        ch.send("What do you wish to set flags on?\n")
        return

    if not arg3:
        ch.send("You need to specify a flag to set.\n")
        return

    if not in_flags:
        ch.send("Which flags do you wish to change?\n")
        return

    if arg1 in ('mob', 'npc', 'character', 'char'):
        victim = ch.get_char_world(arg2)
    else:
        ch.send('You cannot find them.')
        return

    if arg3.startswith('act'):
        if not victim.is_npc():
            ch.send("Use plr for PCs.\n")
            return
        for comp_flag in tables.act_flags.values():
            if not in_flags:
                ch.send('No flags to set.')
                return
            if not comp_flag.name in in_flags:
                ch.send('Flag %s does not exist' % comp_flag.name)
                in_flags.discard(comp_flag.name)
                continue
            else:
                if fequals:
                    for old_flag in victim.act.flags:
                        victim.act.rem_bit(old_flag.bit)
                if fadd or fequals:
                    victim.act.set_bit(comp_flag.bit)
                elif frem:
                    victim.act.rem_bit(comp_flag.bit)
        ch.send('Act flags: {disp_flags}\n Have been set.'.format(disp_flags=(item for item in in_flags)))

    if arg3.startswith('plr'):
        if victim.is_npc():
            ch.send("Use act for NPCs.\n")
            return
        for comp_flag in in_flags:
            if not comp_flag not in tables.plr_flags:
                ch.send('Flag %s does not exist' % comp_flag.name)
                in_flags.discard(comp_flag.name)
                continue
            else:
                if fequals:
                    for old_flag in victim.affected:
                        victim.act.rem_bit(old_flag.bit)
                if fadd or fequals:
                    victim.act.set_bit(tables.plr_flags[comp_flag].bit)
                elif frem:
                    victim.act.rem_bit(tables.plr_flags[comp_flag].bit)
        ch.send('Plr flags: {disp_flags}\n Have been set.'.format(disp_flags=(item for item in in_flags)))

    if arg3.startswith('aff'):
        for comp_flag in tables.affect_flags.values():
            if not in_flags:
                ch.send('No flags to set.')
                return
            if not comp_flag.name in in_flags:
                ch.send('Flag %s does not exist' % comp_flag.name)
                in_flags.discard(comp_flag.name)
                continue
            else:
                if fequals:
                    for old_flag in victim.affected_by.flags:
                        victim.affected_by.rem_bit(old_flag.bit)
                if fadd or fequals:
                    victim.affected_by.set_bit(comp_flag.bit)
                elif frem:
                    victim.affected_by.rem_bit(comp_flag.bit)
        ch.send('Affect flags: {disp_flags}\n Have been set.'.format(disp_flags=(item for item in in_flags)))

    if arg3.startswith('vuln'):
        for comp_flag in tables.imm_flags.values():
            if not in_flags:
                ch.send('No flags to set.')
                return
            if not comp_flag.name in in_flags:
                ch.send('Flag %s does not exist' % comp_flag.name)
                in_flags.discard(comp_flag.name)
                continue
            else:
                if fequals:
                    for old_flag in victim.vuln_flags.flags:
                        victim.vuln_flags.rem_bit(old_flag.bit)
                if fadd or fequals:
                    victim.vuln_flags.set_bit(comp_flag.bit)
                elif frem:
                    victim.vuln_flags.rem_bit(comp_flag.bit)
        ch.send('Vuln flags: {disp_flags}\n Have been set.'.format(disp_flags=(item for item in in_flags)))

    if arg3.startswith('immunity'):
        for comp_flag in tables.imm_flags.values():
            if not in_flags:
                ch.send('No flags to set.')
                return
            if not comp_flag.name in in_flags:
                ch.send('Flag %s does not exist' % comp_flag.name)
                in_flags.discard(comp_flag.name)
                continue
            else:
                if fequals:
                    for old_flag in victim.imm_flags.flags:
                        victim.imm_flags.rem_bit(old_flag.bit)
                if fadd or fequals:
                    victim.imm_flags.set_bit(comp_flag.bit)
                elif frem:
                    victim.imm_flags.rem_bit(comp_flag.bit)
        ch.send('Immunity flags: {disp_flags}\n Have been set.'.format(disp_flags=(item for item in in_flags)))

    if arg3.startswith('resist'):
        for comp_flag in tables.imm_flags.values():
            if not in_flags:
                ch.send('No flags to set.')
                return
            if not comp_flag.name in in_flags:
                ch.send('Flag %s does not exist' % comp_flag.name)
                in_flags.discard(comp_flag.name)
                continue
            else:
                if fequals:
                    for old_flag in victim.res_flags.flags:
                        victim.res_flags.rem_bit(old_flag.bit)
                if fadd or fequals:
                    victim.res_flags.set_bit(comp_flag.bit)
                elif frem:
                    victim.res_flags.rem_bit(comp_flag.bit)
        ch.send('Resist flags: {disp_flags}\n Have been set.'.format(disp_flags=(item for item in in_flags)))

    if arg3.startswith('form'):
        if not victim.is_npc():
            ch.send("Form can't be set on PCs.\n")
            return
        for comp_flag in tables.form_flags.values():
            if not in_flags:
                ch.send('No flags to set.')
                return
            if not comp_flag.name in in_flags:
                ch.send('Flag %s does not exist' % comp_flag.name)
                in_flags.discard(comp_flag.name)
                continue
            else:
                if fequals:
                    for old_flag in victim.form.flags:
                        victim.form_flags.rem_bit(old_flag.bit)
                if fadd or fequals:
                    victim.form_flags.set_bit(comp_flag.bit)
                elif frem:
                    victim.form_flags.rem_bit(comp_flag.bit)
        ch.send('Form flags: {disp_flags}\n Have been set.'.format(disp_flags=(item for item in in_flags)))

    if arg3.startswith('parts'):
        if not victim.is_npc():
            ch.send("Parts can't be set on PCs.\n")
            return
        for comp_flag in tables.part_flags.values():
            if not in_flags:
                ch.send('No flags to set.')
                return
            if not comp_flag.name in in_flags:
                ch.send('Flag %s does not exist' % comp_flag.name)
                in_flags.discard(comp_flag.name)
                continue
            else:
                if fequals:
                    for old_flag in victim.parts.flags:
                        victim.parts.rem_bit(old_flag.bit)
                if fadd or fequals:
                    victim.parts.set_bit(comp_flag.bit)
                elif frem:
                    victim.parts.rem_bit(comp_flag.bit)
        ch.send('Parts flags: {disp_flags}\n Have been set.'.format(disp_flags=(item for item in in_flags)))

    if arg3.startswith('comm'):
        if victim.is_npc():
            ch.send("Comm can't be set on NPCs.\n")
            return
        for comp_flag in tables.comm_flags.values():
            if not in_flags:
                ch.send('No flags to set.')
                return
            if not comp_flag.name in in_flags:
                ch.send('Flag %s does not exist' % comp_flag.name)
                in_flags.discard(comp_flag.name)
                continue
            else:
                if fequals:
                    for old_flag in victim.comm.flags:
                        victim.comm.rem_bit(old_flag.bit)
                if fadd or fequals:
                    victim.comm.set_bit(comp_flag.bit)
                elif frem:
                    victim.comm.rem_bit(comp_flag.bit)
        ch.send('Comm flags: {disp_flags}\n Have been set.'.format(disp_flags=(item for item in in_flags)))

interp.register_command(interp.cmd_type('flag', do_flags, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
