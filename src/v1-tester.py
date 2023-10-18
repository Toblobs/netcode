# Synergy Netcode Framework
# Hosted on @Toblobs GitHub

## Useful Websites:
# https://geeksforgeeks.org/socket-programming-python/?ref=ml_lbp

from __init__ import *
from server import *
from client import *

random_port = randint(49152, 65535)

serv = Server('0.0.0.0', random_port)
serv_thread = threading.Thread(target = serv.start_server, args = (1,), daemon = True)
serv_thread.start()

cli = Client('127.0.0.1', random_port)
cli_thread = threading.Thread(target = cli.start_client, args = (1,), daemon = True)
cli_thread.start()

s_queue_length = 0
c_queue_length = 0

print('Port in use:' + str(random_port))
print()

while True:

    #if len(serv.queue) > s_queue_length:
    #    print(serv.queue[-1])
    #    s_queue_length = serv.queue

    #if len(cli.queue) > c_queue_length:
    #    print(cli.queue[-1])
    #    c_queue_length = cli.queue

    #print(serv.queue)
    #print(cli.queue)

    wait(1) 
        
