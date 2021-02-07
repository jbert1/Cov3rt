from scapy.all import *
from time import *

IP_DST = "10.0.0.4"

msg = []
first = True
start_time = 0
end_time = 0
counter = 0

def PacketHandler(pkt):

    global first
    global start_time
    global end_time
    global counter
    global msg

    end_time = time()

    if pkt.haslayer(IP):
        
        if pkt["IP"].dst == IP_DST:

            if first:
                
                first = False
                counter += 1
                start_time = time()

            else: 
                
                total_time = end_time - start_time

                if total_time > .2:
                    
                    msg.append(counter)
                    counter = 1
                    start_time = time()

                else:
                    
                    counter += 1
                    start_time = time()



def StopFilter(pkt):

    global msg
    global counter

    if pkt.haslayer(IP):

        if(pkt["IP"].dst == IP_DST and pkt["IP"].flags == 0x04):
            
            msg.append(counter)

            return True
    
    return False

x = sniff(iface="eth0", prn=PacketHandler, stop_filter=StopFilter)

output = ""

for char in msg:

    output += chr(char)


print(output)
