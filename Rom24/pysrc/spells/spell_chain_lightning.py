from const import skill_type, SLOT
from fight import damage, is_safe_spell
from merc import act, TO_ROOM, TO_CHAR, TO_VICT, dice, saves_spell, DAM_LIGHTNING, POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_chain_lightning(sn, level, ch, victim, target):
    # H first strike */
    act("A lightning bolt leaps from $n's hand and arcs to $N.", ch, None, victim, TO_ROOM)
    act("A lightning bolt leaps from your hand and arcs to $N.", ch, None, victim, TO_CHAR)
    act("A lightning bolt leaps from $n's hand and hits you! ", ch, None, victim, TO_VICT)

    dam = dice(level, 6)
    if saves_spell(level, victim, DAM_LIGHTNING):
        dam = dam // 3
    damage(ch, victim, dam, sn, DAM_LIGHTNING, True)
    last_vict = victim
    level = level - 4  # decrement damage */

    # new targets */
    while level > 0:
        found = False
        for tmp_vict in ch.in_room.people:
            if not is_safe_spell(ch, tmp_vict, True) and tmp_vict is not last_vict:
                found = True
                last_vict = tmp_vict
                act("The bolt arcs to $n! ", tmp_vict, None, None, TO_ROOM)
                act("The bolt hits you! ", tmp_vict, None, None, TO_CHAR)
                dam = dice(level, 6)
                if saves_spell(level, tmp_vict, DAM_LIGHTNING):
                    dam = dam // 3
                damage(ch, tmp_vict, dam, sn, DAM_LIGHTNING, True)
                level = level - 4  # decrement damage */

        if not found:  # no target found, hit the caster */
            if ch == None:
                return

            if last_vict == ch:  # no double hits */
                act("The bolt seems to have fizzled out.", ch, None, None, TO_ROOM)
                act("The bolt grounds out through your body.", ch, None, None, TO_CHAR)
                return

            last_vict = ch
            act("The bolt arcs to $n...whoops! ", ch, None, None, TO_ROOM)
            ch.send("You are struck by your own lightning! \n")
            dam = dice(level, 6)
            if saves_spell(level, ch, DAM_LIGHTNING):
                dam = dam // 3
            damage(ch, ch, dam, sn, DAM_LIGHTNING, True)
            level = level - 4  # decrement damage */
            if ch == None:
                return


skill_type("chain lightning",
           {'mage': 33, 'cleric': 53, 'thief': 39, 'warrior': 36},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_chain_lightning, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
           None, SLOT(500), 25, 12, "lightning", "!Chain Lightning!", "")