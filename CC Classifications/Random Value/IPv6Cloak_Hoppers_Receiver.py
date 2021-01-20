from scapy.all import *

IP_DST = "ff02::1:ffad:317"
stop_hl = 68
MSG = ''
        

def Sniff_For_Message(pkt):
    if pkt.haslayer(IPv6):
        if (pkt.dst == IP_DST):
            pass

        
def Stop_Sniffing(pkt):
    global MSG
    if (pkt.haslayer(IPv6)):
        MSG += chr(pkt.hlim - 68)
        if (pkt["IPv6"].dst == IP_DST and pkt["IPv6"].hlim == stop_hl):  
            return True
    return False



x = sniff(iface = "Wi-Fi", prn = Sniff_For_Message, stop_filter = Stop_Sniffing)

print ("Secret Message: {}".format(MSG))