import logging
import os
import json

logger = logging.getLogger()

from database.tracker import tables
from settings import DATA_EXTN, DATA_DIR

def write_tables(listener=None, loc=DATA_DIR, extn=DATA_EXTN):
    logger.info('    Writing Tables')

    if listener:
        listener.send("Writing tables\n")
    os.makedirs(loc, 0o755, True)
    for tok in tables:
        path = "%s%s" % (os.path.join(loc, tok.name), extn)
        logger.debug('        Writing %s(%s)', tok.name, path)
        if listener:
            listener.send("\t%s\n" % tok.name)
        write_table(path, tok)

def write_table(path, tok):
    with open(path, 'w') as fp:
        if tok.filter:
            fp.write(json.dumps(tok.filter(tok.table), indent=4, sort_keys=True))
        else:
            fp.write(json.dumps(tok.table, indent=4, sort_keys=True))
