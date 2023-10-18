# Synergy Netcode Framework
# Hosted on @Toblobs GitHub

from __init__ import *

## Useful Websites:
# https://geeksforgeeks.org/socket-programming-python/?ref=ml_lbp

class Client:

    """
        <class '__main__.Client'>

        A class that uses the 'socket' library to send and recieve messages, connect to a server,
        upload shared object to a pool and provide a networking interface.

        Parameters:
        @self | Reference to this Client object.
        @ip | The Internet Protocol Address for this Client object, setting self.ip.
        @port | The Port number for this Client object, setting self.port.

        Instance Variables:
        self.c | This Client's socket.
        self.ip | The IP of this Client object.
        self.port | The Port of this Client object.
        self.queue | Where we place any receieved messages from the server to be processed.
        self.server_key | The public key of the server we are connected to.
        self.input_thread | A thread for inputting messages to be sent to the server.
        self.byte_limit | Maximum amount of bytes per message.
        self.cryptographer | The Crypt() object that handles assymetric decryption and encryption.
        self.alive_time | The delay that the client will send alive packets, in ms.
        self.states | The list of possible client states.
        self.state | The current client state.

    """

    def __init__(self, ip, port):

        self.c = socket.socket()

        self.ip = ip
        self.port = port

        self.queue = []

        self.input_thread = None
        self.server_key = None
        
        self.byte_limit = 2048
        self.cryptographer = Cr()

        self.alive_time = 100 # To be added in #b003

        self.states = ('SETUP', 'RUNNING', 'STOPPED')
        self.state = self.states[0]

    def start_client(self, wastedargs):

        """Starts our client socket, binding to self.ip and self.port,
           and listening for our server socket."""

        self.cryptographer.setup()

        self.c.connect((self.ip, self.port))
        self.loop()

    def stop_client(self):

        """Stops the server socket."""

        self.server_key = None
        self.c.close()

    def loop(self):

        """The main loop of the Client object."""

        # Start thread to send input
        self.input_thread = threading.Thread(target = self.handle_inputs, args = (1,))
        self.input_thread.start() 

        self.state = self.states[1]

        wait(self.alive_time / 100)
        
        self.c.send(self.cryptographer.public_serialized)

        while True:

            try:

                # Receive a message
                byt = self.c.recv(self.byte_limit)
                message = str(byt)

                # Indentity checks to be added in #b002
                if message:

                    #print('[client] external message:' + message)

                    #data = message.split()[1]
                    #print(data)

                    message = self.cryptographer.decrypt(bytes(message, 'utf-8'), self.cryptographer.private_key)
                    self.queue.append(message)

                else:
                    self.remove_connection(conn)

            except:
                continue


    def handle_inputs(self, wastedargs):
        pass
    

                

            
            

        
            
        

        
        
        
