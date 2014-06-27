import merc
import interp


def do_value(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Value what?\n")
        return
    keeper = merc.find_keeper(ch)
    if not keeper:
        return
    obj = ch.get_obj_carry(arg, ch)
    if not obj:
        merc.act("$n tells you 'You don't have that item'.", keeper, None, ch, merc.TO_VICT)
        ch.reply = keeper
        return
    if not keeper.can_see_obj(obj):
        merc.act("$n doesn't see what you are offering.",keeper,None,ch, merc.TO_VICT)
        return
    if not ch.can_drop_obj(obj):
        ch.send("You can't let go of it.\n")
        return
    cost = merc.get_cost(keeper, obj, False)
    if cost <= 0:
        merc.act( "$n looks uninterested in $p.", keeper, obj, ch, merc.TO_VICT)
        return
    merc.act("$n tells you 'I'll give you %d silver and %d gold coins for $p'." % (cost - (cost//100) * 100, cost//100),
      keeper, obj, ch, merc.TO_VICT)
    ch.reply = keeper
    return

interp.cmd_type('value', do_value, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)