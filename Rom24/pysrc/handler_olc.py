__author__ = 'venom'

class AREA_DATA:
    def __init__(self):
        self.reset_list = []
        self.file_name = ""
        self.name = ""
        self.credits = ""
        self.age = 15
        self.nplayer = 0
        self.low_range = 0
        self.high_range = 0
        self.min_vnum = 0
        self.max_vnum = 0
        self.empty = False

    def __repr__(self):
        return "<%s(%s): %d-%d>" % (self.name, self.file_name, self.min_vnum, self.max_vnum)


class EXTRA_DESCR_DATA:
    def __init__(self):
        self.keyword = "" # Keyword in look/examine
        self.description = ""


class EXIT_DATA:
    def __init__(self):
        self.to_room = None
        self.exit_info = 0
        self.key = 0
        self.keyword = ""
        self.description = ""


class RESET_DATA:
    def __init__(self):
        self.command = ""
        self.arg1 = 0
        self.arg2 = 0
        self.arg3 = 0
        self.arg4 = 0


class SHOP_DATA:
    def __init__(self):
        self.keeper = 0
        self.buy_type = {}
        self.profit_buy = 0
        self.profit_sell = 0
        self.open_hour = 0
        self.close_hour = 0

