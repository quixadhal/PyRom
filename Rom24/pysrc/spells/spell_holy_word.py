from const import SLOT, skill_type, skill_table
from fight import damage, is_safe_spell
from merc import act, TO_ROOM, IS_GOOD, IS_EVIL, IS_NEUTRAL, TARGET_CHAR, dice, DAM_ENERGY, POS_FIGHTING, TAR_IGNORE

def spell_holy_word(sn, level, ch, victim, target):
    # RT really nasty high-level attack spell */
    act("$n utters a word of divine power! ", ch, None, None, TO_ROOM)
    ch.send("You utter a word of divine power.\n")

    for vch in ch.in_room.people[:]:
        if (IS_GOOD(ch) and IS_GOOD(vch)) or (IS_EVIL(ch) and IS_EVIL(vch)) or (IS_NEUTRAL(ch) and IS_NEUTRAL(vch)):
            vch.send("You feel full more powerful.\n")
            skill_table['frenzy'].spell_fun('frenzy', level, ch, vch, TARGET_CHAR)
            skill_table['bless'].spell_fun('bless', level, ch, vch, TARGET_CHAR)
        elif (IS_GOOD(ch) and IS_EVIL(vch)) or (IS_EVIL(ch) and IS_GOOD(vch)):
            if not is_safe_spell(ch, vch, True):
                skill_table['curse'].spell_fun('curse', level, ch, vch, TARGET_CHAR)
                vch.send("You are struck down! \n")
                dam = dice(level, 6)
                damage(ch, vch, dam, sn, DAM_ENERGY, True)
        elif IS_NEUTRAL(ch):
            if not is_safe_spell(ch, vch, True):
                skill_table['curse'].spell_fun('curse', level // 2, ch, vch, TARGET_CHAR)
                vch.send("You are struck down! \n")
                dam = dice(level, 4)
                damage(ch, vch, dam, sn, DAM_ENERGY, True)
    ch.send("You feel drained.\n")
    ch.move = 0
    ch.hit = hit // 2

skill_type("holy word",
           { 'mage':53, 'cleric':36, 'thief':53, 'warrior':42 },
           { 'mage':2, 'cleric':2, 'thief':4, 'warrior':4 },
           spell_holy_word, TAR_IGNORE, POS_FIGHTING, None,
           SLOT(506), 200, 24, "divine wrath", "!Holy Word!", "")