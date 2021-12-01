import const
import handler_game
import merc


def spell_fly(sn, level, ch, victim, target):
    if victim.is_affected( merc.AFF_FLYING):
        if victim == ch:
            ch.send("You are already airborne.\n")
        else:
            handler_game.act("$N doesn't need your help to fly.", ch, None, victim, merc.TO_CHAR)
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level + 3
    af.location = 0
    af.modifier = 0
    af.bitvector = merc.AFF_FLYING
    victim.affect_add(af)
    victim.send("Your feet rise off the ground.\n")
    handler_game.act("$n's feet rise off the ground.", victim, None, None, merc.TO_ROOM)
    return


const.register_spell(const.skill_type("fly",
                          {'mage': 10, 'cleric': 18, 'thief': 20, 'warrior': 22},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_fly, merc.TAR_CHAR_DEFENSIVE, merc.POS_STANDING, None,
                          const.SLOT(56), 10, 18, "", "You slowly float to the ground.", ""))
