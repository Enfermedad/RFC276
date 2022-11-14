import time
import socket
import struct
localIP     = "127.0.0.1"
localPort   = 123
NTPFORMAT = ">3B b 3I 4Q"

hz = int(1 / time.clock_getres(time.CLOCK_REALTIME))
precision = 0

print("Calculando...")
#Calcula precision
while hz > 1:
        precision -= 1
        hz >>= 1
print("listo")
####
#UNIX timestamps use as Jan 1 1970 as epoch whereas NTP protocol uses Jan 1 1900
####
#SECONDS 1900 to 1970
NTPDELTA = 2208988800.0
##-----------------------##
def system_to_ntp(t=0.0):
    #------#
    # Transform system timestamp to NTP timestamp
    #------#
    t+= NTPDELTA
    return (int(t) <<32) + (int(abs(t-int(t)*(1<<32))))

'''
def ntp_to_system(x=0):
    #------#
    #Transform NTP timestamp to system timestamp
    #------#
    t = float (x>>32) + float(x & 0xffffffff )/(1<<32)
    return t - NTPDELTA
def tfmt(t = 0.0):
        ###
        #Format System Timestamp
        ###

        return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d_%H:%M:%S.%f")
'''


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
#print("Link Available")

# Listen for incoming datagrams
while(True):
    print("hola")
    data, addr = UDPServerSocket.recvfrom(struct.calcsize(NTPFORMAT))
    serverrecv = system_to_ntp(time.time())
    data = list(data)
    version = data[0] >> 3 & 0x7
    if (version >= 4):
        print("Version mayor que 3")
        break
    mode = data[0] & 0x7
    clienttx = data[10]
    
    data[0] = version << 3 | 4      # Leap, Version, Mode
    data[1] = 0                     # Stratum
    data[2] = 6                     # Poll
    data[3] = precision             # Precision
    data[4] = 0                     # Root delay  
    data[5] = 0                     # Root Dispersion
    data[6] = 0                     # Reference Clock Identifier
    data[7] = serverrecv            # Reference Timestamp
    data[8] = clienttx              # Originate Timestamp
    data[9] = serverrecv            # Receive Timestamp
    data[10] = system_to_ntp(time.time())     # Transmit Timestamp

    # send the response
    data = struct.pack(NTPFORMAT, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10])
    UDPServerSocket.sendto(data, addr)