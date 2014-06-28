import random
from const import SLOT, skill_type
from effects import acid_effect
from fight import damage

from merc import act, TO_NOTVICT, TO_VICT, TO_CHAR, dice, saves_spell, DAM_ACID, TARGET_CHAR, TAR_CHAR_OFFENSIVE, \
    POS_FIGHTING


def spell_acid_breath(sn, level, ch, victim, target):
    # NPC spells.
    act("$n spits acid at $N.", ch, None, victim, TO_NOTVICT)
    act("$n spits a stream of corrosive acid at you.", ch, None, victim, TO_VICT)
    act("You spit acid at $N.", ch, None, victim, TO_CHAR)

    hpch = max(12, ch.hit)
    hp_dam = random.randint(hpch // 11 + 1, hpch // 6)
    dice_dam = dice(level, 16)

    dam = max(hp_dam + dice_dam // 10, dice_dam + hp_dam // 10)

    if saves_spell(level, victim, DAM_ACID):
        acid_effect(victim, level // 2, dam // 4, TARGET_CHAR)
        damage(ch, victim, dam // 2, sn, DAM_ACID, True)
    else:
        acid_effect(victim, level, dam, TARGET_CHAR)
        damage(ch, victim, dam, sn, DAM_ACID, True)


skill_type("acid breath",
           { 'mage':31, 'cleric':32, 'thief':33, 'warrior':34 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_acid_breath, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None,
           SLOT(200), 100, 24, "blast of acid", "!Acid Breath!", "")