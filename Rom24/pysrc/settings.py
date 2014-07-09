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

#extn
DATA_EXTN = '.json'

#Folders
AREA_DIR = os.path.join('..', 'area')
PLAYER_DIR = os.path.join('..', 'player')
DUMP_DIR = os.path.join('..', 'data')
