# CSE310 Programming HW 1
# AUTHOR: Kuba Gasiorowski
# ID: 109776237

# See README.md for details.

import socket
import sys
from enum import Enum
from contextlib import closing

# Server stuff
HOST = ''
DEFAULT_PORT = 8000
PORT = DEFAULT_PORT
HTML_VERSION = 1.1

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
    client.send('HTTP/{0} {1} {2}\n'.format(HTML_VERSION, responseCode, RESPONSE_CODES[responseCode]).encode())

# Main program executes here
if __name__ == '__main__':

    # Catches keyboard interrupts
    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket initialized...")

        # First try to parse a port passed in via cmd line args.
        try:
            
            PORT = int(sys.argv[1])
            print('Using port {0}'.format(PORT))
        
        except:

            PORT = DEFAULT_PORT
            print('Using port {0} (default)'.format(PORT))

        # PORT now has either the custom port or the default
        # Now try to bind the socket
        validPortSelected = False

        try:

            # If the socket correctly binds, then skip the while loop and continue
            print('Trying to bind port {0}...'.format(PORT))
            sock.bind((HOST, PORT))
            validPortSelected = True

        except:

            # If not, then prompt the user for a new port
            print("Error: port {0} could not be bound. Please enter a different port".format(PORT))

        # Continue prompting the user for ports until the socket correctly binds
        while not validPortSelected:

            try:
                
                PORT = int(input('Enter a port:'))
                print('Trying to bind port {0}...'.format(PORT))
                sock.bind((HOST, PORT))
                validPortSelected = True

            except ValueError:
                print("Enter a number please")
            except:
                print("Socket could not be bound, enter a different port")

        print("Success!")    

        sock.listen(5)
        print("Socket now listening...")

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

                cmd = ''

                # Read data character by character until the terminating char is read
                cmd = conn.recv(1024).decode()

                # Echo the entire command in the server
                print(cmd, end='')

                # Split the command into tokens
                tokens = cmd.split()

                tokens[0] = tokens[0].upper()

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
                        conn.send('\n{0}\n'.format(DICTIONARY.get(tokens[1])).encode())

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
                    conn.send(b'Server shutting down!\n')
                    print('Client sent the off signal. Goodbye!')
                    conn.close()
                    sock.close()
                    exit(0)

                else:

                    # Otherwise, send UNSUPPORTED
                    send_response(conn, 220)

    # User pressed ctrl-c. Close everything and exit 
    except KeyboardInterrupt:
        print('User manually quit.')
        try:
            conn.close()
            print("Connection closed...")
        except NameError:
            pass

        try:
            sock.close()
            print("Socket closed...")
        except NameError:
            pass        

        print("Goodbye!")
        exit(0) 
