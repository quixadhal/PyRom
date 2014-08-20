import const
import handler_game
import merc
import state_checks


def spell_invis(sn, level, ch, victim, target):
    # object invisibility */
    if target == merc.TARGET_ITEM:
        obj = victim
        if obj.flags.invis:
            handler_game.act("$p is already invisible.", ch, obj, None, merc.TO_CHAR)
            return

        af = handler_game.AFFECT_DATA()
        af.where = merc.TO_OBJECT
        af.type = sn
        af.level = level
        af.duration = level + 12
        af.location = merc.APPLY_NONE
        af.modifier = 0
        af.bitvector = merc.ITEM_INVIS
        obj.affect_add(af)
        handler_game.act("$p fades out of sight.", ch, obj, None, merc.TO_ALL)
        return
    # character invisibility */
    if victim.is_affected( merc.AFF_INVISIBLE):
        return

    handler_game.act("$n fades out of existence.", victim, None, None, merc.TO_ROOM)
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level + 12
    af.location = merc.APPLY_NONE
    af.modifier = 0
    af.bitvector = merc.AFF_INVISIBLE
    victim.affect_add(af)
    victim.send("You fade out of existence.\n")
    return


const.register_spell(const.skill_type("invisibility",
                          {'mage': 5, 'cleric': 53, 'thief': 9, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_invis, merc.TAR_OBJ_CHAR_DEF, merc.POS_STANDING, None,
                          const.SLOT(29), 5, 12, "", "You are no longer invisible.", "$p fades into view."))
