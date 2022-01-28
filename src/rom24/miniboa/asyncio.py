# -*- coding: utf-8 -*- line endings: unix -*-
# ------------------------------------------------------------------------------
#   miniboa/async.py
#   Copyright 2009 Jim Storch
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain a
#   copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
# ------------------------------------------------------------------------------
# Changes made by pR0Ps.CM[at]gmail[dot]com on 18/07/2012
# -Updated for use with Python 3.x
# -Repackaged into a single file to simplify distribution
# -Other misc fixes and changes
#
# Report any bugs in this implementation to me (email above)
# ------------------------------------------------------------------------------
# Additional changes by Quixadhal on 2014.06.16
# -Re-split code into multiple files, for ease of maintenance
# -Rewrote terminal system
# ------------------------------------------------------------------------------

"""
Handle Asynchronous Telnet Connections.
"""

import socket
import select
import sys
import logging

logger = logging.getLogger(__name__)

from rom24.miniboa.telnet import TelnetClient
from rom24.miniboa.telnet import ConnectionLost


## Cap sockets to 512 on Windows because winsock can only process 512 at time
if sys.platform == "win32":
    MAX_CONNECTIONS = 500
## Cap sockets to 1000 on Linux because you can only have 1024 file descriptors
else:
    MAX_CONNECTIONS = 1000

# --[ Telnet Server ]-----------------------------------------------------------


## Default connection handler
def _on_connect(client):
    """
    Placeholder new connection handler.
    """
    logger.info(
        "++ Opened connection to {}, sending greeting...".format(client.addrport())
    )
    client.send("Greetings from Miniboa-py3!\n")


## Default disconnection handler
def _on_disconnect(client):
    """
    Placeholder lost connection handler.
    """
    logger.info("-- Lost connection to %s", client.addrport())


class TelnetServer(object):
    """
    Poll sockets for new connections and sending/receiving data from clients.
    """

    def __init__(
        self,
        port=23,
        address="",
        on_connect=_on_connect,
        on_disconnect=_on_disconnect,
        max_connections=MAX_CONNECTIONS,
        timeout=0.05,
    ):
        """
        Create a new Telnet Server.

        port -- Port to listen for new connection on.  On UNIX-like platforms,
            you made need root access to use ports under 1025.

        address -- Address of the LOCAL network interface to listen on.  You
            can usually leave this blank unless you want to restrict traffic
            to a specific network device.  This will usually NOT be the same
            as the Internet address of your server.

        on_connect -- function to call with new telnet connections

        on_disconnect -- function to call when a client's connection dies,
            either through a terminated session or client.active being set
            to False.

        max_connections -- maximum simultaneous the server will accept at once

        timeout -- amount of time that Poll() will wait from user input
            before returning.  Also frees a slice of CPU time.
        """

        self.port = port
        self.address = address
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.max_connections = min(max_connections, MAX_CONNECTIONS)
        self.timeout = timeout

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind((address, port))
            server_socket.listen(5)
        except socket.error as err:
            logger.critical("Unable to create the server socket: " + str(err))
            raise

        self.server_socket = server_socket
        self.server_fileno = server_socket.fileno()

        ## Dictionary of active clients,
        ## key = file descriptor, value = TelnetClient instance
        self.clients = {}

    def stop(self):
        """
        Disconnects the clients and shuts down the server
        """
        for clients in self.client_list():
            clients.sock.close()
        self.server_socket.close()
        ## TODO: Anything else need doing?

    def client_count(self):
        """
        Returns the number of active connections.
        """
        return len(self.clients)

    def client_list(self):
        """
        Returns a list of connected clients.
        """
        return self.clients.values()

    def poll(self):
        """
        Perform a non-blocking scan of recv and send states on the server
        and client connection sockets.  Process new connection requests,
        read incomming data, and send outgoing data.  Sends and receives may
        be partial.
        """
        ## Build a list of connections to test for receive data pending
        recv_list = [self.server_fileno]  # always add the server

        del_list = []  # list of clients to delete after polling

        for client in self.clients.values():
            if client.active:
                recv_list.append(client.fileno)
            else:
                self.on_disconnect(client)
                del_list.append(client.fileno)
                client.sock.close()

        ## Delete inactive connections from the dictionary
        for client in del_list:
            del self.clients[client]

        ## Build a list of connections that need to send data
        send_list = []
        for client in self.clients.values():
            if client.send_pending:
                send_list.append(client.fileno)

        ## Get active socket file descriptors from select.select()
        try:
            rlist, slist, elist = select.select(recv_list, send_list, [], self.timeout)
        except select.error as err:
            ## If we can't even use select(), game over man, game over
            logger.critical("SELECT socket error '{}'".format(str(err)))
            raise

        ## Process socket file descriptors with data to receive
        for sock_fileno in rlist:

            ## If it's coming from the server's socket then this is a new
            ## connection request.
            if sock_fileno == self.server_fileno:

                try:
                    sock, addr_tup = self.server_socket.accept()
                except socket.error as err:
                    logger.error("ACCEPT socket error '{}:{}'.".format(err[0], err[1]))
                    continue

                # Check for maximum connections
                if self.client_count() >= self.max_connections:
                    logger.warning("Refusing new connection, maximum already in use.")
                    sock.close()
                    continue

                ## Create the client instance
                new_client = TelnetClient(sock, addr_tup)

                ## Add the connection to our dictionary and call handler
                self.clients[new_client.fileno] = new_client
                self.on_connect(new_client)

            else:
                ## Call the connection's recieve method
                try:
                    self.clients[sock_fileno].socket_recv()
                except ConnectionLost:
                    self.clients[sock_fileno].deactivate()

        ## Process sockets with data to send
        for sock_fileno in slist:
            ## Call the connection's send method
            self.clients[sock_fileno].socket_send()
