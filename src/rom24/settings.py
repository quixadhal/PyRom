import os
import logging
from pathlib import Path


logger = logging.getLogger(__name__)

# Game settings
PORT = 1337
WIZLOCK = False
NEWLOCK = False
ENCRYPT_PASSWORD = True
LOGALL = False
MAX_ITERATIONS = 300

# Files
AREA_LIST = "area.lst"
BUG_FILE = "bug.txt"
TYPO_FILE = "typo.txt"
SOCIAL_LIST = "social.lst"
HELP_FILE = "help_files"

# extn
DATA_EXTN = ".json"
PKL_EXTN = ".pickle"

# Folders
INSTALLED_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SOURCE_DIR = os.path.join(INSTALLED_DIR, "src")
logger.info("SOURCE_DIR: %s", SOURCE_DIR)
LEGACY_AREA_DIR = os.path.join(SOURCE_DIR, "area")
logger.info("LEGACY_AREA_DIR: %s", LEGACY_AREA_DIR)
LEGACY_PLAYER_DIR = os.path.join("../..", "player")
logger.info("LEGACY_PLAYER_DIR: %s", LEGACY_PLAYER_DIR)
SOCIAL_DIR = os.path.join(LEGACY_AREA_DIR, "socials")
logger.info("SOCIAL_DIR: %s", SOCIAL_DIR)
HELP_DIR = os.path.join(LEGACY_AREA_DIR, "help_files")
logger.info("HELP_DIR: %s", HELP_DIR)

# New structure
USER_DIR = os.path.expanduser("~")
BASE_DIR = os.path.join(USER_DIR, "rom24")
DATA_DIR = os.path.join(SOURCE_DIR, "data")
WORLD_DIR = os.path.join(DATA_DIR, "world")
PLAYER_DIR = os.path.join(DATA_DIR, "players")
SYSTEM_DIR = os.path.join(DATA_DIR, "system")
DOC_DIR = os.path.join(DATA_DIR, "docs")
AREA_DIR = LEGACY_AREA_DIR
AREA_LIST_FILE = os.path.join(AREA_DIR, AREA_LIST)
INSTANCE_DIR = os.path.join(WORLD_DIR, "instances")
INSTANCE_NUM_FILE = os.path.join(INSTANCE_DIR, "instance_tracker.txt")
for mydir in (
    BASE_DIR,
    DATA_DIR,
    WORLD_DIR,
    PLAYER_DIR,
    SYSTEM_DIR,
    DOC_DIR,
    AREA_DIR,
    INSTANCE_DIR,
):
    if not os.path.exists(mydir):
        os.makedirs(mydir)

for rom24_file in (INSTANCE_NUM_FILE, AREA_LIST_FILE):
    if not os.path.exists(rom24_file):
        rom24_file_path = Path(rom24_file)
        rom24_file_path.touch(exist_ok=True)

# Features
SHOW_DAMAGE_NUMBERS = True
DETAILED_INVALID_COMMANDS = True
SAVE_LIMITER = 300  # Only save files every N seconds, unless forced.
