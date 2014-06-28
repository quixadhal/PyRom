from const import SLOT, skill_type, register_spell
from fight import damage
from merc import dice, saves_spell, DAM_HARM, POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_harm(sn, level, ch, victim, target):
    dam = max(20, victim.hit - dice(1, 4))
    if saves_spell(level, victim, DAM_HARM):
        dam = min(50, dam // 2)
    dam = min(100, dam)
    damage(ch, victim, dam, sn, DAM_HARM, True)


register_spell(skill_type("harm",
                          {'mage': 53, 'cleric': 23, 'thief': 53, 'warrior': 28},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_harm, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None,
                          SLOT(27), 35, 12, "harm spell", "!Harm!", ""))