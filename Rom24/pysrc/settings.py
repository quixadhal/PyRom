import os


#Game settings
PORT = 1337
WIZLOCK = False
NEWLOCK = False
ENCRYPT_PASSWORD = True
LOGALL = False
MAX_ITERATIONS = 300

#Files
AREA_LIST = 'area.lst'
BUG_FILE = 'bug.txt'
TYPO_FILE = 'typo.txt'
SOCIAL_LIST = 'social.lst'
HELP_FILE = 'help_files'

#extn
DATA_EXTN = '.json'
PKL_EXTN = '.pickle'

#Folders
LEGACY_AREA_DIR = os.path.join('..', 'area')
LEGACY_PLAYER_DIR = os.path.join('..', 'player')
SOCIAL_DIR = os.path.join(LEGACY_AREA_DIR, 'socials')
HELP_DIR = os.path.join(LEGACY_AREA_DIR, 'help_files')

#New structure
DATA_DIR = os.path.join('..', 'data')
WORLD_DIR = os.path.join(DATA_DIR, 'world')

PLAYER_DIR = os.path.join(DATA_DIR, 'players')
SYSTEM_DIR = os.path.join(DATA_DIR, 'system')
DOC_DIR = os.path.join(DATA_DIR, 'docs')

AREA_DIR = os.path.join(WORLD_DIR, 'areas')
INSTANCE_DIR = os.path.join(WORLD_DIR, 'instances')

#Features
SHOW_DAMAGE_NUMBERS = True
DETAILED_INVALID_COMMANDS = True
