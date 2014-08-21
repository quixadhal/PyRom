import const
import fight
import game_utils
import handler_ch
import handler_game
import handler_magic
import merc
import state_checks


def spell_charm_person(sn, level, ch, victim, target):
    if fight.is_safe(ch, victim):
        return

    if victim == ch:
        ch.send("You like yourself even better! \n")
        return

    if ( victim.is_affected( merc.AFF_CHARM) \
                 or ch.is_affected(merc.AFF_CHARM) \
                 or level < victim.level \
                 or state_checks.IS_SET(victim.imm_flags, merc.IMM_CHARM) \
                 or handler_magic.saves_spell(level, victim, merc.DAM_CHARM) ):
        return

    if state_checks.IS_SET(victim.in_room.room_flags, merc.ROOM_LAW):
        ch.send("The mayor does not allow charming in the city limits.\n")
        return

    if victim.master:
        handler_ch.stop_follower(victim)
    handler_ch.add_follower(victim, ch)
    victim.leader = ch
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = game_utils.number_fuzzy(level // 4)
    af.location = 0
    af.modifier = 0
    af.bitvector = merc.AFF_CHARM
    victim.affect_add(af)
    #TODO: Known broken. Mob will immediately try to fight you after casting this, because this is an offensive spell.
    #ROM had some stipulation to prevent this combat, possibly in fight.py:is_safe()
    handler_game.act("Isn't $n just so nice?", ch, None, victim, merc.TO_VICT)
    if ch is not victim:
        handler_game.act("$N looks at you with adoring eyes.", ch, None, victim, merc.TO_CHAR)


const.register_spell(const.skill_type("charm person",
                          {'mage': 20, 'cleric': 53, 'thief': 25, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_charm_person, merc.TAR_CHAR_OFFENSIVE, merc.POS_STANDING,
                          None, const.SLOT(7), 5, 12, "", "You feel more self-confident.", "")
)
