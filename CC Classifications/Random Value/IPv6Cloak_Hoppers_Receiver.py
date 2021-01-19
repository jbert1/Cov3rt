from scapy.all import *

Decoded_Message = []
IP_DST = "ff02::1:ffad:317"
stop_hl = 68

def Stop_Sniffing(pkt):
    if pkt.haslayer(IPv6):
        if (pkt["IPv6"].dst == IP_DST and pkt["IPv6"].hlim == stop_hl):
            return True
    return False
        

def Sniff_For_Message(pkt):
    global Decoded_Message
    i = 0
    if pkt.haslayer(IPv6):
        if (pkt.dst == IP_DST):
            Decoded_Message[i] = ord(pkt.hlim)


def Decode_Message(pkt):
    print Decoded_Message


x = sniff(iface = "Wi-Fi", prn = Sniff_For_Message, stop_filter = Stop_Sniffing)