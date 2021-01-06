from scapy.all import *
from sys import stdout

IP_DST = "10.0.0.4"
S_PORT = 12345
D_PORT = 23456

# Packet handler
def PacketHandler(pkt):
    # IPv4 with UDP
    if (pkt.haslayer(UDP) and pkt.haslayer(IP) and pkt.haslayer(Raw)):
        # Correct Options
        if (pkt["IP"].dst == IP_DST and pkt["UDP"].sport == S_PORT and pkt["UDP"].dport == D_PORT):
            length = len(pkt["Raw"].load)
            if length != 4:
                stdout.write(chr(length))
    stdout.flush()

def StopFilter(pkt):
    # IPv4 with UDP
    if (pkt.haslayer(UDP) and pkt.haslayer(IP) and pkt.haslayer(Raw)):
        # Correct Options
        if (pkt["IP"].dst == IP_DST and pkt["UDP"].sport == S_PORT and pkt["UDP"].dport == D_PORT):
            length = len(pkt["Raw"].load)
            if length == 4:
                return True
    return False

x = sniff(iface="Wi-Fi", prn=PacketHandler, stop_filter=StopFilter)