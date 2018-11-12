import os
import struct
import socket
import time
import sys
import select

DEFAULT_HOSTNAME = "google.com"
DEFAULT_TIMEOUT = 1000 # In milliseconds
DEFAULT_PACKETCOUNT = 10

total_packets = 0
dropped_packets = 0
receivedPackets = 0;
avgRTT = 0
maxRTT = 0
minRTT = minRTTinit = 99999999999999


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


# Main code to ping a destination address, with timeout timeout tries times.
def verbose_ping(hostname, timeout, tries):

    addr = socket.gethostbyname(hostname)
    print("Pinging {0} ({1}) {2} times (timeout: {3}ms)...".format(hostname, addr, tries, timeout))
 
    for i in range(tries):
        # Send a packet and record the time

        icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))  
        icmp_sock.settimeout(timeout/1000)

        sendTime = 0
        receiveTime = 0
        packet = create_packet()
        timeoutFlag = False

        # Send the packet and record the time
        icmp_sock.sendto(packet, (addr, 1))
        sendTime = time.time()
  
        # Recieve a packet and record the time
        try:
            packet, addr_ = icmp_sock.recvfrom(2048)
        except socket.timeout:
            timeoutFlag = True

        # If it timed out ignore the reception time
        if timeoutFlag:
            receiveTime = None
        else:
            receiveTime = time.time()

        # Get the data (for debugging)
        # data = packet[28:]
        # print("Data received: {0}".format(data.decode()))

        # Take the difference and print it
        if(receiveTime is None):  
            RTTinMS = None
            print("Packet {0}: Timeout".format(i+1))
        else:
            RTTinMS = round((receiveTime - sendTime)*1000.0,2)
            print("Packet {0}: {1}ms".format(i+1, RTTinMS))

        icmp_sock.close()
        updateStats(RTTinMS)
        time.sleep(1)

# Update our ping statistics
def updateStats(RTT):
    global total_packets
    global dropped_packets
    global receivedPackets
    global minRTT
    global maxRTT
    global avgRTT

    total_packets+=1
    if RTT is None:
        dropped_packets+=1
    else:

        receivedPackets += 1
        avgRTT += (RTT-avgRTT) / (receivedPackets)

        if RTT < minRTT:
            minRTT = RTT
        elif RTT > maxRTT:
            maxRTT = RTT


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
    except socket.gaierror:
        print("No ip could be found for this hostname ({0})".format(hostname))
        exit() 
    except KeyboardInterrupt:
        print("\nInterrupted")

    print("-----------------------------")
    print("Min RTT: {0}ms, Max RTT: {1}ms, Avg RTT: {2}ms".format(0 if minRTT == minRTTinit else minRTT , maxRTT, round(avgRTT,2)))
    print("{0} packets transmitted, {1} received, {2}% packet loss".format(total_packets, total_packets-dropped_packets, round(dropped_packets/total_packets*100.0, 2)))

