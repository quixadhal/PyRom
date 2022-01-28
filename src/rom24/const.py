from collections import OrderedDict, namedtuple
import logging

from typing import *

logger = logging.getLogger(__name__)

spell_lookup_dict: Dict[str, Any] = {}

race_type = namedtuple(
    "race_type", "name, pc_race, act, aff, off, imm, res, vuln, form, parts"
)
race_table: Dict[str, Any] = OrderedDict()

pc_race_type = namedtuple(
    "pc_race_type", "name, who_name, points, class_mult, skills, stats, max_stats, size"
)
pc_race_table: Dict[str, Any] = OrderedDict()


def SLOT(i):
    return i


skill_type = namedtuple(
    "skill_type",
    "name, skill_level, rating, spell_fun, "
    "target, minimum_position, pgsn, slot, "
    "min_mana, beats, noun_damage, msg_off, msg_obj",
)
skill_table: Dict[str, Any] = OrderedDict()


def register_spell(entry: skill_type):
    skill_table[entry.name] = entry
    spell_lookup_dict[entry.name] = [entry.slot]
    logger.debug("    %s  %d added to lookup", entry.name, entry.slot)
    logger.debug("    %s registered in skill table.", entry.name)


group_type = namedtuple("group_type", "name, rating, spells")
group_table: Dict[str, Any] = OrderedDict()

guild_type = namedtuple(
    "guild_type",
    "name, who_name, attr_prime, weapon, guild_rooms, "
    "skill_adept, thac0_00, thac0_32, hp_min, hp_max, "
    "fMana, base_group, default_group",
)
guild_table: Dict[str, Any] = OrderedDict()

weapon_type = namedtuple("weapon_type", "name, vnum, type, gsn")
weapon_table: Dict[str, Any] = OrderedDict()

title_table: Dict[str, Any] = {}

# * Attribute bonus structures.
str_app_type = namedtuple("str_app_type", "tohit, todam, carry, wield")
str_app: Dict[str, Any] = OrderedDict()

int_app_type = namedtuple("int_app_type", "learn")
int_app: Dict[str, Any] = OrderedDict()

wis_app_type = namedtuple("wis_app_type", "practice")
wis_app: Dict[str, Any] = OrderedDict()

dex_app_type = namedtuple("dex_app_type", "defensive")
dex_app: Dict[str, Any] = OrderedDict()

con_app_type = namedtuple("con_app_type", "hitp, shock")
con_app: Dict[str, Any] = OrderedDict()


# /* attack table  -- not very organized :( */
attack_type = namedtuple("attack_type", "name, noun, damage")
attack_table: Dict[str, Any] = OrderedDict()


wiznet_type = namedtuple("wiznet_type", "name bit level")
wiznet_table: Dict[str, Any] = OrderedDict()

liq_type = namedtuple("liq_type", "name color proof full thirst food ssize")
liq_table: Dict[str, Any] = OrderedDict()
