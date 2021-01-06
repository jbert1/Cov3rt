from scapy.all import *
from sys import stdout

IP_DST = "10.0.0.4"
MSG = ''

# Decode binary text
def BinaryDecoder(binary):
    # Initialize string
    string = ''
    # Loop over the data
    for i in range(0, len(binary), 8):
        c = "0b{}".format(binary[i:i + 8])
        string = string + chr(int(c, 2))
    return string


# Packet handler
def PacketHandler(pkt):
    global MSG
    # IPv4
    if pkt.haslayer(IP):
        # Correct Options
        if pkt["IP"].dst == IP_DST:
            if pkt["IP"].flags == 0x00:
                MSG += '0'
                stdout.write('0')
            elif pkt["IP"].flags == 0x04:
                MSG += '1'
                stdout.write('1')
    stdout.flush()

def StopFilter(pkt):
    # IPv4 with UDP and DNS
    if pkt.haslayer(IP):
        # Correct Options
        if (pkt["IP"].dst == IP_DST and pkt["IP"].flags == 0x06):
            return True
    return False


x = sniff(iface="Wi-Fi", prn=PacketHandler, stop_filter=StopFilter)

print()
print(BinaryDecoder(MSG))