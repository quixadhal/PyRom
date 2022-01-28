import os
import importlib
import traceback
import logging
from typing import *

logger = logging.getLogger(__name__)

# dictionary of files to track. will be key'd by file name and the value will be modified unix timestamp
tracked_files: Dict[str, int] = {}
modified_files: Dict[str, int] = {}


# Looks like we need to fix the directory for this init so that it will find the commands.


def init_file(path, modules):
    # called by init_monitoring to begin tracking a file.
    logger.info("Initializing monitoring for %s: %s", path, modules)
    loaded_modules = {m: importlib.import_module(m) for m in modules}
    logger.info("Adding %s to tracked paths.", path)
    tracked_files[path] = [os.path.getmtime(path), loaded_modules]
    logger.info("Successfully initialized %s", path)


def init_module(module):
    logger.info("Initializing module for %s", module)
    loaded_module = importlib.import_module(f"rom24.{module}")
    tracked_files[loaded_module.__file__] = os.path.getmtime(loaded_module.__file__)


def init_directory_module(directory_module):
    loaded_module = importlib.import_module(f"rom24.{directory_module}")
    dirpath = os.path.dirname(loaded_module.__file__)
    dir_items = os.listdir(dirpath)
    dfiles = [f for f in dir_items if not f.startswith("__")]

    logger.info("Tracking %d files in %s", len(dfiles), dirpath)
    for dfile in dfiles:
        dfmodule = f"{directory_module}.{dfile.split('.')[0]}"
        init_module(dfmodule)


def init_monitoring():
    # Called in main function to begin tracking files.
    logger.info("Monitoring system initializing...")
    modules_to_init = [
        "handler_ch",
        "handler_item",
        "handler_room",
        "shop_utils",
        "game_utils",
        "pyprogs",
        "affects",
        "effects",
    ]
    directories_to_init = ["commands", "spells"]
    for module in modules_to_init:
        init_module(module)
    for directory in directories_to_init:
        init_directory_module(directory)
    logger.info("done. (Monitoring system)")


def poll_files():
    # Called in game_loop of program to check if files have been modified.
    for fp, mod in tracked_files.items():
        if mod != os.path.getmtime(fp):
            # File has been modified.
            logger.warn("%s has been modified", fp)
            tracked_files[fp] = os.path.getmtime(fp)
            modified_files[fp] = os.path.getmtime(fp)


def reload_files(ch):
    # This will be broken - we need to import the module again
    # but we're just doing file path and load times - we can
    # infer the module from the file path though.
    for fp, mod in modified_files.copy().items():
        import_path = fp.split("src")[-1]
        module_name = import_path.replace("/", ".").lstrip(".").split(".py")[0]
        module = importlib.import_module(module_name)
        logger.warn("Reloading %s from %s", module, fp)
        try:
            importlib.reload(module)
        except:
            ch.send(traceback.format_exc())
            logger.exception("Failed to reload %s", fp)

        del modified_files[fp]
