import time
import socket
import struct
localIP     = "127.0.0.1"
localPort   = 123
NTPFORMAT = "!B B B b 11I"

hz = int(1 / time.clock_getres(time.CLOCK_REALTIME))
acc = 0

print("Calculando precision...")
#Calcula precision
while hz > 1:
        acc -= 1
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

def to_time(integ, frac, n=32):
    return integ + float(frac)/2**n	

def to_frac(timestamp, n=32):
    return int(abs(timestamp - _to_int(timestamp)) * 2**n)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
#print("Link Available")

# Listen for incoming datagrams
while(True):
    data, addr = UDPServerSocket.recvfrom(struct.calcsize(NTPFORMAT))
    serverrecv = system_to_ntp(time.time())
    data = list(data)
    
    #Desempaquetar valores
    leap = data[0] >> 6 & 0x3
    version = data[0] >> 3 & 0x7
    mode = data[0] & 0x7
    stratum = data[1]
    poll = data[2]
    precision = data[3]
    root_delay = float(data[4]/2**16)
    root_dispersion = float(data[5])/2**16
    ref_id = data[6]
    ref_timestamp = to_time(data[7], data[8])
    orig_timestamp = to_time(data[9], data[10])
    recv_timestamp = to_time(data[11], data[12])
    tx_timestamp = to_time(data[13], data[14])

    #Procesar valores
    leap = 0
    mode = 4
    stratum = 2             #Referencia secundaria
    precision = acc
    root_delay = 0
    root_dispersion = 0     #calcular segun shoa
    ref_id = 0xc81b6a73     #200.27.106.115 to hex
    ref_timestamp= serverrecv
    recv_timestamp = serverrecv
    tx_timestamp = system_to_ntp(time.time())
    
    # Enviar respuesta
    data = struct.pack(NTPFORMAT, leap << 6 | version << 3 | mode, stratum, poll, precision, int(root_delay) << 16 | to_frac(root_delay,16),
     int(root_dispersion) << 16 | to_frac(root_dispersion,16), ref_id, int(ref_timestamp), to_frac(ref_timestamp), int(orig_timestamp), to_frac(orig_timestamp),
     int(recv_timestamp), to_frac(recv_timestamp), int(tx_timestamp), to_frac(tx_timestamp))
    
    UDPServerSocket.sendto(data, addr)