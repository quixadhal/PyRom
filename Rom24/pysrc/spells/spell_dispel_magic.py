from const import SLOT, skill_type, register_spell
import const
from merc import saves_spell, DAM_OTHER, check_dispel, act, TO_ROOM, IS_AFFECTED, AFF_SANCTUARY, saves_dispel, \
    is_affected, REMOVE_BIT, POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_dispel_magic(sn, level, ch, victim, target):
    # modified for enhanced use */
    if saves_spell(level, victim, DAM_OTHER):
        victim.send("You feel a brief tingling sensation.\n")
        ch.send("You failed.\n")
        return

    spells = {'armor': None,
              'bless': None,
              'blindness': '$n is no longer blinded',
              'calm': '$n no longer looks so peaceful...',
              'change sex': '$n looks more like $mself again.',
              'charm person': '$n regains $s free will.',
              'chill touch': '$n looks warmer',
              'curse': None,
              'detect evil': None,
              'detect good': None,
              'detect hidden': None,
              'detect invis': None,
              'detect magic': None,
              'faerie fire': "$n's outline fades",
              'fly': '$n falls to the ground! ',
              'frenzy': "$n no longer looks so wild.",
              'giant strength': "$n no longer looks so mighty.",
              'haste': '$n is no longer moving so quickly',
              'infravision': None,
              'invis': '$n fades into existence.',
              'mass invis': '$n fades into existence',
              'pass door': None,
              'protection evil': None,
              'protection good': None,
              'sanctuary': "The white aura around $n's body vanishes.",
              'shield': 'The shield protecting $n vanishes',
              'sleep': None,
              'slow': '$n is no longer moving so slowly.',
              'stone skin': "$n's skin regains its normal texture.",
              'weaken': "$n looks stronger."}

    for k, v in spells.items():
        if check_dispel(level, victim, const.skill_table[k]):
            if v:
                act(v, victim, None, None, TO_ROOM)
            found = True

    if IS_AFFECTED(victim, AFF_SANCTUARY) and not saves_dispel(level, victim.level, -1) and not is_affected(victim,
                                                                                                            const.skill_table[
                                                                                                                "sanctuary"]):
        REMOVE_BIT(victim.affected_by, AFF_SANCTUARY)
        act("The white aura around $n's body vanishes.", victim, None, None, TO_ROOM)
        found = True

    if found:
        ch.send("Ok.\n")
    else:
        ch.send("Spell failed.\n")


register_spell(skill_type("dispel magic",
                          {'mage': 16, 'cleric': 24, 'thief': 30, 'warrior': 30},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_dispel_magic, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
                          None, SLOT(59), 15, 12, "", "!Dispel Magic!", ""))