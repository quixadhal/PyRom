import random
import const
import db
import handler_game
import handler_obj
import merc
import state_checks


def spell_floating_disc(sn, level, ch, victim, target):
    floating = ch.get_eq(merc.WEAR_FLOAT)
    if floating and state_checks.IS_OBJ_STAT(floating, merc.ITEM_NOREMOVE):
        handler_game.act("You can't remove $p.", ch, floating, None, merc.TO_CHAR)
        return

    disc = db.create_object(merc.obj_index_hash[merc.OBJ_VNUM_DISC], 0)
    disc.value[0] = ch.level * 10  # 10 pounds per level capacity */
    disc.value[3] = ch.level * 5  # 5 pounds per level max per item */
    disc.timer = ch.level * 2 - random.randint(0, level // 2)

    handler_game.act("$n has created a floating black disc.", ch, None, None, merc.TO_ROOM)
    ch.send("You create a floating disc.\n")
    disc.to_char(ch)
    handler_obj.wear_obj(ch, disc, True)


const.register_spell(const.skill_type("floating disc",
                          {'mage': 4, 'cleric': 10, 'thief': 7, 'warrior': 16},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_floating_disc, merc.TAR_IGNORE, merc.POS_STANDING, None,
                          const.SLOT(522), 40, 24, "", "!Floating disc!", ""))
