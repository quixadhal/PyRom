import merc
import interp
import tables
import handler

def do_mstat(ch, argument):
    argument, arg = merc.read_word( argument )
    if not arg:
        ch.send("Stat whom?\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    ch.send("Name: %s\n" % victim.name)
    ch.send("Vnum: %d  Format: %s  Race: %s  Group: %d  Sex: %s  Room: %d\n" % (
                0 if not merc.IS_NPC(victim) else victim.pIndexData.vnum,
                "pc" if not merc.IS_NPC(victim) else "new" if victim.pIndexData.new_format else "old",
                victim.race.name,
                0 if not merc.IS_NPC(victim) else victim.group, tables.sex_table[victim.sex],
                0 if not victim.in_room else victim.in_room.vnum ) )

    if merc.IS_NPC(victim):
        ch.send("Count: %d  Killed: %d\n" % (victim.pIndexData.count,victim.pIndexData.killed))
    ch.send("Str: %d(%d)  Int: %d(%d)  Wis: %d(%d)  Dex: %d(%d)  Con: %d(%d)\n" % (
                victim.perm_stat[merc.STAT_STR], victim.get_curr_stat(merc.STAT_STR),
                victim.perm_stat[merc.STAT_INT], victim.get_curr_stat(merc.STAT_INT),
                victim.perm_stat[merc.STAT_WIS], victim.get_curr_stat(merc.STAT_WIS),
                victim.perm_stat[merc.STAT_DEX], victim.get_curr_stat(merc.STAT_DEX),
                victim.perm_stat[merc.STAT_CON], victim.get_curr_stat(merc.STAT_CON)))
    ch.send("Hp: %d/%d  Mana: %d/%d  Move: %d/%d  Practices: %d\n" % (
                victim.hit, victim.max_hit,
                victim.mana, victim.max_mana,
                victim.move, victim.max_move,
                0 if merc.IS_NPC(ch) else victim.practice ) )
    ch.send("Lv: %d  Class: %s  Align: %d  Gold: %ld  Silver: %ld  Exp: %d\n" % (
                victim.level,
                "mobile" if IS_NPC(victim) else victim.guild.name,
                victim.alignment, victim.gold, victim.silver, victim.exp ) )
    ch.send("Armor: pierce: %d  bash: %d  slash: %d  magic: %d\n" % (
                merc.GET_AC(victim,AC_PIERCE), merc.GET_AC(victim,AC_BASH),
                merc.GET_AC(victim,AC_SLASH),  merc.GET_AC(victim,AC_EXOTIC)))
    ch.send("Hit: %d  Dam: %d  Saves: %d  Size: %s  Position: %s  Wimpy: %d\n" % (
                merc.GET_HITROLL(victim), merc.GET_DAMROLL(victim), victim.saving_throw,
                tables.size_table[victim.size], tables.position_table[victim.position].name,
                victim.wimpy ))
    if merc.IS_NPC(victim) and victim.pIndexData.new_format:
        ch.send("Damage: %dd%d  Message:  %s\n" % (
              victim.damage[merc.DICE_NUMBER],victim.damage[merc.DICE_TYPE],
              const.attack_table[victim.dam_type].noun) )
    ch.send("Fighting: %s\n" % (victim.fighting.name if victim.fighting else "(none)" ))
    if not merc.IS_NPC(victim):
        ch.send( "Thirst: %d  Hunger: %d  Full: %d  Drunk: %d\n" % (
                    victim.pcdata.condition[merc.COND_THIRST],
                    victim.pcdata.condition[merc.COND_HUNGER],
                    victim.pcdata.condition[merc.COND_FULL],
                    victim.pcdata.condition[merc.COND_DRUNK] ))
    ch.send("Carry number: %d  Carry weight: %ld\n" % (victim.carry_number, merc.get_carry_weight(victim) // 10 ))
    if not merc.IS_NPC(victim):
        ch.send("Age: %d  Played: %d  Last Level: %d  Timer: %d\n",
                    victim.get_age(), (int) (victim.played + time.time() - victim.logon) // 3600,
                    victim.pcdata.last_level, victim.timer )
    ch.send("Act: %s\n" % handler.act_bit_name(victim.act))
    if victim.comm:
        ch.send("Comm: %s\n" % handler.comm_bit_name(victim.comm))
    if IS_NPC(victim) and victim.off_flags:
        ch.send("Offense: %s\n" % handler.off_bit_name(victim.off_flags))
    if victim.imm_flags:
        ch.send("Immune: %s\n" % handler.imm_bit_name(victim.imm_flags))
    if victim.res_flags:
        ch.send("Resist: %s\n" % handler.imm_bit_name(victim.res_flags))
    if victim.vuln_flags:
        ch.send("Vulnerable: %s\n" % handler.imm_bit_name(victim.vuln_flags))
    ch.send("Form: %s\nParts: %s\n" % (handler.form_bit_name(victim.form), handler.part_bit_name(victim.parts)))
    if victim.affected_by:
        ch.send("Affected by %s\n" % handler.affect_bit_name(victim.affected_by))
    ch.send("Master: %s  Leader: %s  Pet: %s\n" % (
                victim.master.name if victim.master else "(none)",
                victim.leader.name if victim.leader else "(none)",
                victim.pet.name if victim.pet else "(none)"))
    ch.send("Short description: %s\nLong  description: %s" % (  victim.short_descr,
                victim.long_descr if victim.long_descr else "(none)\n" ) )
    if merc.IS_NPC(victim) and victim.spec_fun != None:
        ch.send("Mobile has special procedure %s.\n" % victim.spec_fun.__name__)

    for paf in victim.affected:
        ch.send("Spell: '%s' modifies %s by %d for %d hours with bits %s, level %d.\n" % (
                    paf.type,
                    affect_loc_name(paf.location),
                    paf.modifier,
                    paf.duration,
                    handler.affect_bit_name(paf.bitvector),
                    paf.level))

interp.cmd_type('mstat', do_mstat, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1)