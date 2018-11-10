import os
import struct
import socket
import time
import subprocess

def create_icmp_socket():
   return sock

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

# This code builds a packet. 'data' is the data in the field
def create_packet(): 
  ICMP_TYPE=8 # Indicates an echo request
  ICMP_CODE=0 # Indicates a ping reply
  ID=os.getpid()&0xFFFF # The ID will be set the ID of your running program. Since we are only given so much space, we only use the first 2 bytes
  SEQUENCE=1 # You don't have to continuously communicate with the server. By setting the SEQ number to 1, we can treat all attempts as separate.
  CHECKSUM=0 
  data = bytes(str(time.time()), "utf-8");
  header = struct.pack("bbHHh", ICMP_TYPE, ICMP_CODE, CHECKSUM, ID, SEQUENCE)
  CHECKSUM=checksum(header+data)
  header = struct.pack("bbHHh", ICMP_TYPE, ICMP_CODE, CHECKSUM, ID, SEQUENCE)
  packet=header+data
  return packet

def send_one_ping(sock, addr):
  
  packet = create_packet()
  sock.sendto(packet, (addr, 1))
  return time.time()
  

def recieve_one_ping(sock, timeout):

  packet, addr = sock.recvfrom(2048)
  timeRecieved = time.time()

  data = packet[28:]

  print("Data recieved: {0}".format(data.decode()))

  return timeRecieved
 

# Main code to ping a destination address, with timeout timeout tries times.
def verbose_ping(hostname, timeout, tries):
  
  icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))  

  try:
    destination_IP = socket.gethostbyname(hostname)
  except socket.gaierror:
    print("No ip could be found for this hostname ({0})".format(hostname))
    return
  
  for i in range(tries):
    # Send a packet and record the time
    
    # print("Sending packet {0}: {1}, [{2}]".format(i+1, destination_IP, packet))
    print("Sending packet {0}".format(i+1))
    sendTime = send_one_ping(icmp_sock, destination_IP)
    
    # Recieve a packet and record the time
    recieveTime = recieve_one_ping(icmp_sock, timeout) 

    # Take the difference and print it
    if(recieveTime is None):  
      print("Timeout!")
    else:
      print("{0}ms\n".format(round((recieveTime - sendTime)*1000.0,2)))

    time.sleep(1)


# Main program
if __name__ == '__main__':

  # Some basic testing constants
  sample_hostname = "google.com"
  sample_timeout = 1
  sample_tries = 5

  # Call the ping function
  verbose_ping(sample_hostname, sample_timeout, sample_tries)
 
  print("Everything worked!")
 
