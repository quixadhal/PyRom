import const
import handler_game
import handler_magic
import merc
import state_checks


def spell_slow(sn, level, ch, victim, target):
    if state_checks.is_affected(victim, sn) or victim.is_affected( merc.AFF_SLOW):
        if victim == ch:
            ch.send("You can't move any slower! \n")
        else:
            handler_game.act("$N can't get any slower than that.", ch, None, victim, merc.TO_CHAR)
        return

    if handler_magic.saves_spell(level, victim, merc.DAM_OTHER) or state_checks.IS_SET(victim.imm_flags, merc.IMM_MAGIC):
        if victim != ch:
            ch.send("Nothing seemed to happen.\n")
        victim.send("You feel momentarily lethargic.\n")
        return

    if victim.is_affected( merc.AFF_HASTE):
        if not handler_magic.check_dispel(level, victim, const.skill_table['haste']):
            if victim != ch:
                ch.send("Spell failed.\n")
            victim.send("You feel momentarily slower.\n")
            return
        handler_game.act("$n is moving less quickly.", victim, None, None, merc.TO_ROOM)
        return

    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level // 2
    af.location = merc.APPLY_DEX
    af.modifier = -1 - (level >= 18) - (level >= 25) - (level >= 32)
    af.bitvector = merc.AFF_SLOW
    victim.affect_add(af)
    victim.send("You feel yourself slowing d o w n...\n")
    handler_game.act("$n starts to move in slow motion.", victim, None, None, merc.TO_ROOM)


const.register_spell(const.skill_type("slow",
                          {'mage': 23, 'cleric': 30, 'thief': 29, 'warrior': 32},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_slow, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING, None,
                          const.SLOT(515), 30, 12, "", "You feel yourself speed up.", ""))
