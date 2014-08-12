import const
import handler_game
import handler_magic
import merc
import state_checks


def spell_remove_curse(sn, level, ch, victim, target):
    found = False
    # do object cases first */
    if target == merc.TARGET_ITEM:
        obj = victim

        if state_checks.is_item_stat(obj, merc.ITEM_NODROP) or state_checks.is_item_stat(obj, merc.ITEM_NOREMOVE):
            if not state_checks.is_item_stat(obj, merc.ITEM_NOUNCURSE) and not handler_magic.saves_dispel(level + 2, obj.level, 0):
                state_checks.REMOVE_BIT(obj.extra_flags, merc.ITEM_NODROP)
                state_checks.REMOVE_BIT(obj.extra_flags, merc.ITEM_NOREMOVE)
                handler_game.act("$p glows blue.", ch, obj, None, merc.TO_ALL)
                return
            handler_game.act("The curse on $p is beyond your power.", ch, obj, None, merc.TO_CHAR)
            return

        handler_game.act("There doesn't seem to be a curse on $p.", ch, obj, None, merc.TO_CHAR)
        return

    # characters */
    if handler_magic.check_dispel(level, victim, const.skill_table['curse']):
        victim.send("You feel better.\n")
        handler_game.act("$n looks more relaxed.", victim, None, None, merc.TO_ROOM)

    for obj in victim.contents:
        if (state_checks.is_item_stat(obj, merc.ITEM_NODROP) or state_checks.is_item_stat(obj,
                                                                                        merc.ITEM_NOREMOVE)) and not state_checks.is_item_stat(obj,
                                                                                                                                              merc.ITEM_NOUNCURSE):
            # attempt to remove curse */
            if not handler_magic.saves_dispel(level, obj.level, 0):
                state_checks.REMOVE_BIT(obj.extra_flags, merc.ITEM_NODROP)
                state_checks.REMOVE_BIT(obj.extra_flags, merc.ITEM_NOREMOVE)
                handler_game.act("Your $p glows blue.", victim, obj, None, merc.TO_CHAR)
                handler_game.act("$n's $p glows blue.", victim, obj, None, merc.TO_ROOM)
                break


const.register_spell(const.skill_type("remove curse",
                          {'mage': 53, 'cleric': 18, 'thief': 53, 'warrior': 22},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_remove_curse, merc.TAR_OBJ_CHAR_DEF, merc.POS_STANDING,
                          None, const.SLOT(35), 5, 12, "", "!Remove Curse!", ""))
