import json
import logging
import os

from rom24.settings import DATA_DIR, DATA_EXTN
from rom24.database.tracker import tables


logger = logging.getLogger(__name__)


def read_tables(listener=None, loc=DATA_DIR, extn=DATA_EXTN):
    if listener:
        # This means the game is running. Wipe the current data.
        logger.debug("Clearing all tables.")
        for tok in tables:
            logger.debug("    Clearing %s.", tok.name)
            if not tok.filter:
                tok.table.clear()
            else:
                affected = tok.filter(tok.table)
                for k, v in tok.table.copy().items():
                    if k in affected:
                        del tok.table[k]

        listener.send("Tables cleared. Rebuilding...\n")
    logger.info("    Loading Tables.")
    for tok in tables:
        path = "%s%s" % (os.path.join(loc, tok.name), extn)
        logger.debug("        Loading %s(%s)", tok.name, path)
        data = None
        if os.path.isfile(path):
            data = json.load(open(path, "r"))
        else:
            logger.warning("    Failed to find file %s", path)
            if listener:
                listener.send("Failed to load %s" % path)
            continue
        try:
            for k, v in data.items():
                if type(k) == str and k.isdigit():
                    k = int(k)
                if tok.tupletype:
                    tok.table[k] = tok.tupletype._make(v)
                else:
                    tok.table[k] = v
        except (AttributeError):  # Its a list
            for v in data:
                tok.table.append(v)
