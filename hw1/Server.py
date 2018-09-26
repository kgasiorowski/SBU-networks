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


DICTIONARY = {}


# Prints a response to the screen
def send_response(client, responseCode):
    client.send('HTTP/1.1 {0} {1}\n'.format(responseCode, RESPONSE_CODES[responseCode]).encode())


if __name__ == '__main__':

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

        while True:

            charRead = ''
            cmd = ''

            # Read data character by character until the terminating char is read
            while charRead != TERMINATING_CHAR:
                cmd += charRead
                charRead = conn.recv(1024).decode()

            # Main program stuff goes here

            print(cmd)

            tokens = cmd.split()
            cmd = tokens[0]

            if cmd == Command.GET.value:

                if len(tokens) <= 1:
                    send_response(conn, 400)

                elif tokens[1] not in DICTIONARY:
                    send_response(conn, 404)

                else:

                    send_response(conn, 200)
                    conn.send('\n\n{0}'.format(DICTIONARY.get(tokens[1])).encode())

            elif cmd == Command.PUT.value:

                if len(tokens) <= 2:
                    send_response(conn, 400)

                else:

                    DICTIONARY[tokens[1]] = tokens[2]
                    send_response(conn, 200)


            elif cmd == Command.CLEAR.value:

                DICTIONARY.clear()
                send_response(conn, 200)

            elif cmd == Command.DELETE.value:

                if len(tokens) <= 1:
                    send_response(conn, 400)
                    continue

                if tokens[1] in DICTIONARY:
                    del DICTIONARY[tokens[1]]

                send_response(conn, 200)

            elif cmd == Command.QUIT.value:

                send_response(conn, 200)
                break

            else:

                send_response(conn, 220)

        conn.close()
