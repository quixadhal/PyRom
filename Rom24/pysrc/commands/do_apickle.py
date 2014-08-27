__author__ = 'syn'

import logging

logger = logging.getLogger()

import os
import interp
import merc
import save
import settings


def do_apickle(ch, argument):
    ch.send("Saving areas to pickle format..\n\n")
    save.area_pickler()
    open(os.path.join(settings.LEGACY_AREA_DIR, settings.PAREA_LIST), 'w').close()  # lets write a clean list
    open(os.path.join(settings.LEGACY_AREA_DIR, settings.SOCIAL_LIST), 'w').close()
    with open(os.path.join(settings.LEGACY_AREA_DIR, settings.PAREA_LIST), 'a') as alf:
        ch.send("Writing Area List...\n\n")
        for area in merc.area_list:
            als = ("%s\n" % area.name)
            alf.write(als)
        alf.write("$")
        alf.close()
        ch.send("Area List Saved.\n\n")
    with open(os.path.join(settings.LEGACY_AREA_DIR, settings.SOCIAL_LIST), 'a') as slf:
        ch.send("Writing Social List...\n\n")
        for social in merc.social_list:
            sls = ("%s\n" % social.name)
            slf.write(sls)
        slf.write("$")
        slf.close()
        ch.send("Social List Saved.\n\n")
    return

interp.register_command(interp.cmd_type('apickle', do_apickle, merc.POS_DEAD, merc.ML, merc.LOG_ALWAYS, 1))

