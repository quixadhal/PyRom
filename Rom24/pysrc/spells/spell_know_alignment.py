import const
import handler_game
import merc


def spell_know_alignment(sn, level, ch, victim, target):
    ap = victim.alignment

    if ap > 700:
        msg = "$N has a pure and good aura."
    elif ap > 350:
        msg = "$N is of excellent moral character."
    elif ap > 100:
        msg = "$N is often kind and thoughtful."
    elif ap > -100:
        msg = "$N doesn't have a firm moral commitment."
    elif ap > -350:
        msg = "$N lies to $S friends."
    elif ap > -700:
        msg = "$N is a black-hearted murderer."
    else:
        msg = "$N is the embodiment of pure evil! ."

    handler_game.act(msg, ch, None, victim, merc.TO_CHAR)
    return


const.register_spell(const.skill_type("know alignment",
                          {'mage': 12, 'cleric': 9, 'thief': 20, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_know_alignment, merc.TAR_CHAR_DEFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(58), 9, 12, "", "!Know Alignment!", ""))
