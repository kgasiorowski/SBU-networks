import socket
from sys import exit
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
    OFF = 'OFF'

DICTIONARY = {}


# Prints a response to the screen
def send_response(client, responseCode):
    client.send('HTTP/1.1 {0} {1}\n'.format(responseCode, RESPONSE_CODES[responseCode]).encode())


if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket initialized")

    sock.bind((HOST, PORT))
    print("Socket bound to port {0}".format(PORT))

    sock.listen(5)
    print("Socket now listening")

    # Continue to accept connections until the loop is broken out of
    while True:

        # Wait for a connection
        conn, addr = sock.accept()
        print("Connected to {0}".format(addr))
        conn.send(b"Enter input:")

        cmd = ''

        # Continue to get input on the current connection until
        # QUIT or OFF breaks out of the loop
        while True:

            charRead = ''
            cmd = ''

            # Read data character by character until the terminating char is read
            while charRead != TERMINATING_CHAR:
                cmd += charRead
                charRead = conn.recv(1024).decode()

            # Echo the entire command in the server
            print(cmd)

            # Split the command into tokens
            tokens = cmd.split()

            # If no tokens are parsed, return UNSUPPORTED
            if len(tokens) < 1:
                send_response(conn, 220)
                continue

            # The actual command should be the first token
            cmd = tokens[0]

            if cmd == Command.GET.value:

                # Send BAD REQUEST if there is not enough tokens
                if len(tokens) <= 1:
                    send_response(conn, 400)

                # Return not found if the requested key is not found
                elif tokens[1] not in DICTIONARY:
                    send_response(conn, 404)

                # Or send OK and the dictionary value retrieved
                else:

                    send_response(conn, 200)
                    conn.send('\n\n{0}'.format(DICTIONARY.get(tokens[1])).encode())

            elif cmd == Command.PUT.value:

                # BAD REQUEST if there are not exactly 3 tokens
                if len(tokens) != 3:
                    send_response(conn, 400)

                # Otherwise update the dictionary and send OK
                else:

                    DICTIONARY[tokens[1]] = tokens[2]
                    send_response(conn, 200)


            elif cmd == Command.CLEAR.value:

                # Dictionary should always be cleared and send OK
                DICTIONARY.clear()
                send_response(conn, 200)

            elif cmd == Command.DELETE.value:

                # There must be at least 2 tokens, otherwise send BAD REQUEST
                if len(tokens) <= 1:
                    send_response(conn, 400)
                    continue

                # IF the key exists in dictionary, delete it
                if tokens[1] in DICTIONARY:
                    del DICTIONARY[tokens[1]]

                # Always send OK
                send_response(conn, 200)

            elif cmd == Command.QUIT.value:

                # Send OK, close this connection, and wait for a new one
                send_response(conn, 200)
                conn.close()
                break

            elif cmd == Command.OFF.value:

                # Send OK, close the connection and socket, and shut down the server
                send_response(conn, 200)
                conn.send(b'Server shutting down!');
                conn.close()
                sock.close()
                exit(0)

            else:

                # Otherwise, send UNSUPPORTED
                send_response(conn, 220)
