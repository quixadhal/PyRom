from rom24.const import (
    liq_table,
    wiznet_table,
    attack_table,
    con_app,
    dex_app,
    wis_app,
    int_app,
    str_app,
    title_table,
    weapon_table,
    guild_table,
    group_table,
    pc_race_table,
    race_table,
    skill_table,
    pc_race_type,
    race_type,
    liq_type,
    wiznet_type,
    attack_type,
    dex_app_type,
    wis_app_type,
    int_app_type,
    str_app_type,
    weapon_type,
    guild_type,
    group_type,
    skill_type,
    con_app_type,
)
from rom24.tables import (
    comm_flags,
    part_flags,
    form_flags,
    imm_flags,
    off_flags,
    affect_flags,
    plr_flags,
    act_flags,
    size_table,
    sex_table,
    position_table,
    clan_table,
    clan_type,
    position_type,
    flag_type,
    exit_flags,
)


def skill_filter(table):
    return {k: v for k, v in table.items() if not v.spell_fun}


class SaveToken:
    def __init__(self, name, table, tupletype, filter=None):
        self.name = name
        self.table = table
        self.tupletype = tupletype
        self.filter = filter


tables = [
    SaveToken("clan_table", clan_table, clan_type),
    SaveToken("position_table", position_table, position_type),
    SaveToken("sex_table", sex_table, None),
    SaveToken("size_table", size_table, None),
    SaveToken("act_flags", act_flags, flag_type),
    SaveToken("plr_flags", plr_flags, flag_type),
    SaveToken("affect_flags", affect_flags, flag_type),
    SaveToken("off_flags", off_flags, flag_type),
    SaveToken("imm_flags", imm_flags, flag_type),
    SaveToken("form_flags", form_flags, flag_type),
    SaveToken("part_flags", part_flags, flag_type),
    SaveToken("comm_flags", comm_flags, flag_type),
    SaveToken("race_table", race_table, race_type),
    SaveToken("pc_race_table", pc_race_table, pc_race_type),
    SaveToken("skill_table", skill_table, skill_type, skill_filter),
    SaveToken("group_table", group_table, group_type),
    SaveToken("guild_table", guild_table, guild_type),
    SaveToken("weapon_table", weapon_table, weapon_type),
    SaveToken("title_table", title_table, None),
    SaveToken("str_app", str_app, str_app_type),
    SaveToken("int_app", int_app, int_app_type),
    SaveToken("wis_app", wis_app, wis_app_type),
    SaveToken("dex_app", dex_app, dex_app_type),
    SaveToken("con_app", con_app, con_app_type),
    SaveToken("attack_table", attack_table, attack_type),
    SaveToken("wiznet_table", wiznet_table, wiznet_type),
    SaveToken("liq_table", liq_table, liq_type),
    SaveToken("exit_flags", exit_flags, flag_type),
]
