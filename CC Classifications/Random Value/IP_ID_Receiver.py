from scapy.all import *

IP_DST = "10.10.10.10"
stop_id = 42069
MSG = ''
        

def Sniff_For_Message(pkt):
    
    if pkt.haslayer(IP):
        if (pkt.dst == IP_DST):
            pass

        
def Stop_Sniffing(pkt):
    global MSG
    if (pkt.haslayer(IP)):
        if(pkt["IP"].dst == IP_DST and pkt["IP"].id != stop_id):
            MSG += chr(pkt.id)
            
        if (pkt["IP"].dst == IP_DST and pkt["IP"].id == stop_id):  
            return True
    return False



x = sniff(iface = "Wi-Fi", prn = Sniff_For_Message, stop_filter = Stop_Sniffing)

print ("Secret Message: {}".format(MSG))