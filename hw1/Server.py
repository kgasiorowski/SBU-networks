import socket
from enum import Enum

# Server stuff
HOST = ''
PORT = 8000

# The char that signifies the end of a command
TERMINATING_CHAR = '|'

# Dictionary for all our response codes
RESPONSE_CODES = {
    200: 'OK',
    220: 'UNSUPPORTED',
    400: 'BAD_REQUEST',
    404: 'NOT_FOUND'
}

# Enum to hold all our commands
class Command(Enum):
    GET = 'GET'
    PUT = 'PUT'
    DELETE = 'DELETE'
    CLEAR = 'CLEAR'
    QUIT = 'QUIT'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket initialized")

sock.bind((HOST, PORT))
print("Socket bound to port %s" % PORT)

sock.listen(5)
print("Socket now listening")

while True:

    conn, addr = sock.accept()
    print("Connected to {0}".format(addr))
    conn.send(b"Enter a message:")

    cmd = ''

    while cmd != Command.QUIT:

        charRead = ''
        cmd = ''

        # Read data character by character until the terminating char is read
        while charRead != TERMINATING_CHAR:

            cmd += charRead
            charRead = conn.recv(64).decode()

        # Main program stuff goes here

        print(cmd)

    conn.close()
