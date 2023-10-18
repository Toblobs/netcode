# Synergy Netcode Framework
# Hosted on @Toblobs GitHub

from __init__ import *

## Useful Websites:
# https://geeksforgeeks.org/socket-programming-python/?ref=ml_lbp

class Server:

    """
       <class '__main__.Server'>

       A class that uses the 'socket' library to send and receive messages, maintain connections
       with clients, upload shared objects to a pool and provide a networking interface.

       Parameters:
       @self | Reference to this Server object.
       @ip | The Internet Protocol Address for this Server object, setting self.ip.
       @port | The Port number for this Server object, setting self.port.
       @max_c | The maximum amount of clients that can connect, setting self.max_clients.

       Instance Variables:
       self.s | This Server's socket.
       self.ip | The IP of this Server object.
       self.port | The Port of this Server object.
       self.queue | Where we place any received messages from clients to be processed.
       self.max_clients | The maximum amount of clients that can connect to self.s.
       self.clients | A list of all the clients connected.
       self.client_threads | A list of all the client threads.
       self.public_keys | A dictionary of all of the conn / public key pairs.
       self.byte_limit | Maximum amount of bytes per message.
       self.cryptographer | The Crypt() object that handles assymetric decryption and encryption.
       self.alive_time | The delay until kick when a client stops sending still-alive packets, in ms.
       self.states | The list of possible server states.
       self.state | The current server state.

    """

    def __init__(self, ip, port, max_c = 100):

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.ip = ip
        self.port = port

        self.queue = []
        
        self.max_clients = max_c
        self.clients = []
        self.client_threads = []

        self.public_keys = {}

        self.byte_limit = 2048
        self.cryptographer = Cr()

        self.alive_time = 500 # To be added in #b003

        self.states = ('SETUP', 'RUNNING', 'STOPPED')
        self.state = self.states[0]
        
    def start_server(self, wastedargs):

        """Starts our server socket, binding to self.ip and self.port,
           and listening for self.max_clients amount of clients."""

        self.cryptographer.setup()

        self.s.bind((self.ip, self.port))
        self.s.listen(self.max_clients)

        self.loop()

    def stop_server(self):

        """Stops the server socket."""

        for conn in self.clients:
            conn.close()

        self.clients = []
        self.public_keys = []
        self.s.close()

    def handle_client(self, conn, addr):

        """Handles a singular client thread and listens for that client.

           Parameters:
           @conn | The connection to our client.
           @addr | The IP address (relative) of our client."""

        # Send public key to client
        conn.send(self.cryptographer.public_serialized)

        while True:

            try:

                # Recieve a message
                byt = conn.recv(self.byte_limit)
                message = str(byt)

                # Identity checks to be added in #b002
                if message:

                    #print('[server] external message:' + message)

                    this_client_key = self.cryptographer.deserialize_pu_key(message)
                    #print(this_client_key)
                    self.public_keys[conn] = this_client_key
                    #print(self.public_keys)
                            
                    message = self.cryptographer.decrypt_message(bytes(message, 'utf-8'), self.cryptographer.private_key)
                            
                    self.queue.append(message)

                else:
                    self.remove_connection(conn)

            except:
                continue

    def send_message(message, conn):

        """Sends a message to the client with connection <conn>. Uses the public key provided by
           that client to send messages.

           Parameters:
           @message | The message we want to send.
           @conn | The connection for the client we are dealing with."""

        if conn in self.public_keys.keys:

            pu_key = self.public_key[conn]
            encrypted_message = self.cryptographer.encrypt_message(bytes(message, 'utf-8'), pu_key)
            conn.send(bytes(encrypted_message, 'utf-8'))

    def broadcast_message(message, conns_to_remove = []):

        """Sends a message to every client in our self.clients list, bar any in the conns_to_remove list.

           Parameters:
           @message | The message we want to send.
           @conns_to_remove | Any connections we want to exclude from the broadcast."""

        for cli in self.clients:
            if cli not in conns_to_remove:
                self.send_message(message, cli)

        
    def remove_connection(conn):

        """Removes a connection from our self.clients instance variable list, if it's in the list.

           Parameters:
           @conn | The connection we want to remove."""

        if conn in self.clients:
            self.clients.remove(conn)

    def loop(self):

        """The main loop of the Server object."""

        self.state = self.states[1]

        while True:

            # Accept connection
            conn, addr = self.s.accept()
            self.clients.append(conn)

            # Start thread
            self.client_threads.append(threading.Thread(target = self.handle_client, args = (conn, addr)))
            self.client_threads[-1].start()

        self.stop_server()

    
           

        

    
       

    
    
