from scapy.all import *
from sys import stdout

IP_DST = "8.8.8.8"
DOMAIN = "google.com" + "."
STOP_DOMAIN = "ourgourdandsavior.com" + '.'
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
    # IPv4 with UDP and DNS
    if (pkt.haslayer(UDP) and pkt.haslayer(IP) and pkt.haslayer(DNS) and pkt.haslayer(DNSQR)):
        # Correct Options
        if (pkt["IP"].dst == IP_DST and pkt["DNS"].rd == 1 and pkt["DNSQR"].qname.lower() == DOMAIN.encode()):
            if pkt["DNSQR"].qname == DOMAIN.lower().encode():
                MSG += '0'
                stdout.write('0')
            elif pkt["DNSQR"].qname == DOMAIN.upper().encode():
                MSG += '1'
                stdout.write('1')
    stdout.flush()

def StopFilter(pkt):
    # IPv4 with UDP and DNS
    if (pkt.haslayer(UDP) and pkt.haslayer(IP) and pkt.haslayer(DNS) and pkt.haslayer(DNSQR)):
        # Correct Options
        if (pkt["IP"].dst == IP_DST and pkt["DNS"].rd == 1 and pkt["DNSQR"].qname == STOP_DOMAIN.encode()):
            return True
    return False


x = sniff(iface="Wi-Fi", prn=PacketHandler, stop_filter=StopFilter)

print()
print(BinaryDecoder(MSG))