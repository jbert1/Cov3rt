from scapy.all import *

IP_DST = "10.0.0.4"
msg = []

def PacketHandler(pkt):

    global msg

    if pkt.haslayer(TCP):

        if pkt["IP"].dst == IP_DST and pkt["IP"].flags != 0x06:

            msg.append(pkt["TCP"].seq)

def StopFilter(pkt):

    if pkt.haslayer(IP):

        if pkt["IP"].dst == IP_DST and pkt["IP"].flags == 0x04:
            
            return True

    return False


x = sniff(iface="eth0", prn=PacketHandler, stop_filter=StopFilter)

output = ""

for char in msg:
    output += chr(char)

print(output)
