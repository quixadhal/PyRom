import logging


logger = logging.getLogger()
from bit import Bit
from const import skill_type, str_app
import handler_game
from merc import TO_OBJECT, TO_WEAPON, TO_AFFECTS, TO_IMMUNE, TO_RESIST, TO_VULN, APPLY_NONE, APPLY_STR, STAT_STR, \
    APPLY_DEX, STAT_DEX, APPLY_INT, STAT_INT, APPLY_WIS, STAT_WIS, APPLY_CON, STAT_CON, APPLY_SEX, APPLY_CLASS, \
    APPLY_LEVEL, APPLY_AGE, APPLY_HEIGHT, APPLY_WEIGHT, APPLY_MANA, APPLY_HIT, APPLY_MOVE, APPLY_GOLD, APPLY_EXP, \
    APPLY_AC, APPLY_HITROLL, APPLY_DAMROLL, APPLY_SAVES, APPLY_SAVING_ROD, APPLY_SAVING_PETRI, APPLY_SAVING_BREATH, \
    APPLY_SAVING_SPELL, APPLY_SPELL_AFFECT, WEAR_WIELD, TO_CHAR, TO_ROOM
from tables import affect_flags


class Affects:
    def __init__(self):
        super().__init__()
        self.affected = []
        self.affected_by = Bit(flags=affect_flags)

    def is_affected(self, aff):
        if isinstance(aff, skill_type):
            aff = aff.name
        if type(aff) == str:
            return True if [paf for paf in self.affected if paf.type == aff][:1] else False
        return self.affected_by.is_set(aff)

    def affect_add(self, paf):
        paf_new = handler_game.AFFECT_DATA()
        paf_new.__dict__ = paf.__dict__.copy()
        self.affected.append(paf_new)
        self.affect_modify(paf_new, True)
        return


    # * Add or enhance an affect.
    def affect_join(self, paf):
        for paf_old in self.affected:
            if paf_old.type == paf.type:
                paf.level = (paf.level + paf_old.level) / 2
                paf.duration += paf_old.duration
                paf.modifier += paf_old.modifier
                self.affect_remove(paf_old)
                break

        self.affect_add(paf)
        return
    # * Remove an affect from a char.
    def affect_remove(self, paf):
        if not self.affected:
            logger.error("BUG: Affect_remove: no affect.")
            return

        self.affect_modify(paf, False)
        where = paf.where
        vector = paf.bitvector

        if paf not in self.affected:
            logger.error("Affect_remove: cannot find paf.")
            return
        self.affected.remove(paf)
        del paf
        self.affect_check(where, vector)
        return

    def affect_check(self, where, vector):
        if where in [TO_OBJECT, TO_WEAPON] or not vector:
            return

        for paf in self.affected:
            if paf.where == where and paf.bitvector == vector:
                if where == TO_AFFECTS:
                    self.affected_by.set_bit(vector)
                elif where == TO_IMMUNE:
                    self.imm_flags.set_bit(vector)
                elif where == TO_RESIST:
                    self.res_flags.set_bit(vector)
                elif where == TO_VULN:
                    self.vuln_flags.set_bit(vector)
                return

        for obj in self.contents:
            if obj.wear_loc == -1:
                continue
            for paf in obj.affected:
                if paf.where == where and paf.bitvector == vector:
                    if where == TO_AFFECTS:
                        self.affected_by.set_bit(vector)
                    elif where == TO_IMMUNE:
                        self.imm_flags.set_bit(vector)
                    elif where == TO_RESIST:
                        self.res_flags.set_bit(vector)
                    elif where == TO_VULN:
                        self.vuln_flags.set_bit(vector)
                    return
            if obj.enchanted:
                continue
            for paf in obj.pIndexData.affected:
                if paf.where == where and paf.bitvector == vector:
                    if where == TO_AFFECTS:
                        self.affected_by.set_bit(vector)
                    elif where == TO_IMMUNE:
                        self.imm_flags.set_bit(vector)
                    elif where == TO_RESIST:
                        self.res_flags.set_bit(vector)
                    elif where == TO_VULN:
                        self.vuln_flags.set_bit(vector)
                    return

    # * Apply or remove an affect to a character.
    def affect_modify(self, paf, fAdd):
        mod = paf.modifier
        if fAdd:
            if paf.where == TO_AFFECTS:
                self.affected_by.set_bit(paf.bitvector)
            elif paf.where == TO_IMMUNE:
                self.imm_flags.set_bit(paf.bitvector)
            elif paf.where == TO_RESIST:
                self.res_flags.set_bit(paf.bitvector)
            elif paf.where == TO_VULN:
                self.vuln_flags.set_bit(paf.bitvector)
        else:
            if paf.where == TO_AFFECTS:
                self.affected_by.rem_bit(paf.bitvector)
            elif paf.where == TO_IMMUNE:
                self.imm_flags.rem_bit(paf.bitvector)
            elif paf.where == TO_RESIST:
                self.res_flags.rem_bit(paf.bitvector)
            elif paf.where == TO_VULN:
                self.vuln_flags.rem_bit(paf.bitvector)
            mod = 0 - mod

        if paf.location == APPLY_NONE:
            pass
        elif paf.location == APPLY_STR:
            self.mod_stat[STAT_STR] += mod
        elif paf.location == APPLY_DEX:
            self.mod_stat[STAT_DEX] += mod
        elif paf.location == APPLY_INT:
            self.mod_stat[STAT_INT] += mod
        elif paf.location == APPLY_WIS:
            self.mod_stat[STAT_WIS] += mod
        elif paf.location == APPLY_CON:
            self.mod_stat[STAT_CON] += mod
        elif paf.location == APPLY_SEX:
            self.sex += mod
        elif paf.location == APPLY_CLASS:
            pass
        elif paf.location == APPLY_LEVEL:
            pass
        elif paf.location == APPLY_AGE:
            pass
        elif paf.location == APPLY_HEIGHT:
            pass
        elif paf.location == APPLY_WEIGHT:
            pass
        elif paf.location == APPLY_MANA:
            self.max_mana += mod
        elif paf.location == APPLY_HIT:
            self.max_hit += mod
        elif paf.location == APPLY_MOVE:
            self.max_move += mod
        elif paf.location == APPLY_GOLD:
            pass
        elif paf.location == APPLY_EXP:
            pass
        elif paf.location == APPLY_AC:
            for i in range(4):
                self.armor[i] += mod
        elif paf.location == APPLY_HITROLL:
            self.hitroll += mod
        elif paf.location == APPLY_DAMROLL:
            self.damroll += mod
        elif paf.location == APPLY_SAVES:
            self.saving_throw += mod
        elif paf.location == APPLY_SAVING_ROD:
            self.saving_throw += mod
        elif paf.location == APPLY_SAVING_PETRI:
            self.saving_throw += mod
        elif paf.location == APPLY_SAVING_BREATH:
            self.saving_throw += mod
        elif paf.location == APPLY_SAVING_SPELL:
            self.saving_throw += mod
        elif paf.location == APPLY_SPELL_AFFECT:
            pass
        else:
            logger.error("Affect_modify: unknown location %d." % paf.location)
            return
        #
        # * Check for weapon wielding.
        # * Guard against recursion (for weapons with affects).
        wield = self.get_eq(WEAR_WIELD)
        if not self.is_npc() and wield \
                and wield.get_weight() > (str_app[self.stat(STAT_STR)].wield * 10):
            global depth

            if depth == 0:
                depth += 1
                handler_game.act("You drop $p.", self, wield, None, TO_CHAR)
                handler_game.act("$n drops $p.", self, wield, None, TO_ROOM)
                wield.from_char()
                wield.to_room(self.in_room)
                depth -= 1
        return