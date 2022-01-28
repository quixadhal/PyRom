import os
import sys
import logging

logger = logging.getLogger(__name__)

from rom24.miniboa import TelnetServer
from rom24.settings import PORT
from rom24.comm import game_loop, init_descriptor, close_socket
from rom24.hotfix import init_monitoring
import time

startup_time = time.time()


def pyom():
    sys.path.append(os.getcwd())
    logger.info("Logging system initialized.")
    server = TelnetServer(port=PORT)
    server.on_connect = init_descriptor
    server.on_disconnect = close_socket

    # TODO: Fix file monitoring
    init_monitoring()
    logger.info("Entering Game Loop")
    game_loop(server)
    logger.critical("System halted.")


if __name__ == "__main__":
    pyom()
