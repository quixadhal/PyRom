from const import SLOT, skill_type, register_spell
from merc import IS_AFFECTED, AFF_BLIND, target_name, POS_STANDING, TAR_IGNORE


def spell_farsight(sn, level, ch, victim, target):
    if IS_AFFECTED(ch, AFF_BLIND):
        ch.send("Maybe it would help if you could see?\n")
        return

    ch.do_scan(target_name)


register_spell(skill_type("farsight",
                          {'mage': 14, 'cleric': 16, 'thief': 16, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_farsight, TAR_IGNORE, POS_STANDING, None,
                          SLOT(521), 36, 20, "farsight", "!Farsight!", ""))