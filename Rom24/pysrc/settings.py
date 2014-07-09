import os


#Game settings
PORT = 1337
WIZLOCK = False
NEWLOCK = False
ENCRYPT_PASSWORD = True
LOGALL = False

#Files
AREA_LIST = 'area.lst'
PAREA_LIST = 'area2.lst'
BUG_FILE = 'bug.txt'
TYPO_FILE = 'typo.txt'
SOCIAL_LIST = 'social.lst'
HELP_FILE = 'help_files'

#extn
DATA_EXTN = '.json'
PKL_EXTN = '.pickle'

#Folders
AREA_DIR = os.path.join('..', 'area')
SOCIAL_DIR = os.path.join(AREA_DIR, 'socials')
HELP_DIR = os.path.join(AREA_DIR, 'help_files')
PLAYER_DIR = os.path.join('..', 'player')
DUMP_DIR = os.path.join('..', 'data')
