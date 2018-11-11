import os
import struct
import socket
import time
import sys
import select

DEFAULT_HOSTNAME = "google.com"
DEFAULT_TIMEOUT = 1000 # In milliseconds
DEFAULT_PACKETCOUNT = 5

# Taken from piazza
# Creates the checksum
def checksum(source_string):
    sum = 0
    countTo = int(len(source_string)/2)*2
    count = 0
    while count<countTo:
        thisVal = source_string[count + 1]*256 + source_string[count]
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count = count + 2
    if countTo<len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff
    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    # answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

# Also taken from piazza
def create_packet(): 
  ICMP_TYPE=8 # Indicates an echo request
  ICMP_CODE=0 # Indicates a ping reply
  ID=os.getpid()&0xFFFF # The ID will be set the ID of your running program. Since we are only given so much space, we only use the first 2 bytes
  SEQUENCE=1 # You don't have to continuously communicate with the server. By setting the SEQ number to 1, we can treat all attempts as separate.
  CHECKSUM=0 
  data = bytes(str(time.time()), "utf-8"); # Set the creation time of this packet as the data
  header = struct.pack("bbHHh", ICMP_TYPE, ICMP_CODE, CHECKSUM, ID, SEQUENCE)
  CHECKSUM=checksum(header+data)
  header = struct.pack("bbHHh", ICMP_TYPE, ICMP_CODE, CHECKSUM, ID, SEQUENCE)
  packet=header+data
  return packet

# Sends a single packet to the socket, returning the timestamp
def send_one_ping(sock, addr):
  
  packet = create_packet()
  sock.sendto(packet, (addr, 1))
  return time.time()
  
# Recieves one single packet from the socket, and returns the timestamp
def receive_one_ping(sock):

  try:
    packet, addr = sock.recvfrom(2048)
  except socket.timeout:
    return

  timeRecieved = time.time()

  data = packet[28:]

  # print("Data received: {0}".format(data.decode()))

  return timeRecieved
 

# Main code to ping a destination address, with timeout timeout tries times.
def verbose_ping(hostname, timeout, tries):

  icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))  
  icmp_sock.settimeout(timeout/1000.0)

  try:
    destination_IP = socket.gethostbyname(hostname)
  except socket.gaierror:
    print("No ip could be found for this hostname ({0})".format(hostname))
    return
 
  print("Pinging {0} ({1}) {2} times (timeout: {3}ms)...".format(hostname, destination_IP, tries, timeout))
 
  for i in range(tries):
    # Send a packet and record the time
    
    # print("Sending packet {0}: {1}, [{2}]".format(i+1, destination_IP, packet))
    sendTime = send_one_ping(icmp_sock, destination_IP)
    # print("Sent packet {0}".format(i+1))
    
    # Recieve a packet and record the time
    receiveTime = receive_one_ping(icmp_sock) 

    # Take the difference and print it
    if(receiveTime is None):  
      print("Packet {0}: Timeout".format(i+1))
    else:
      print("Packet {0}: {1}ms".format(i+1, round((receiveTime - sendTime)*1000.0,2)))

    time.sleep(1)

if __name__ == '__main__':

  try:
    hostname = sys.argv[1]  
  except IndexError:
    hostname = DEFAULT_HOSTNAME

  try:
    timeout = float(sys.argv[2])
  except IndexError:
    timeout = DEFAULT_TIMEOUT
  except ValueError:
    print("Invalid value for timeout")
    exit()

  try:
    packetcount = int(sys.argv[3])
  except IndexError:
    packetcount = DEFAULT_PACKETCOUNT
  except ValueError:
    print("Invalid packet count")
    exit()

  # Call the ping function
  try:
    verbose_ping(hostname, timeout, packetcount)
  except KeyboardInterrupt:
    print("\nInterrupted")
 
