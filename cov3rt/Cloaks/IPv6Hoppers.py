from scapy.all import *

from logging import error
from re import search
from time import sleep

from cov3rt.Cloaks.Cloak import Cloak

'''
VARIABLES REQUIRED
IPv6 Source (ip_src)
IPv6 Destination (ip_dst)
EOT Hop Limit (EOT_hl) (MUST be set between 64 and 128)
'''

class IPv6Hoppers(Cloak):
    
    #To whoever wants to read this, I'm sorry
    IPv6_REGEX = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"


    def __init__(self, EOT_hl = 69, ip_src = "fe80::1461:beca:7ad:3167", ip_dst = "ff02::1:ffad:317"):
        self.classification = Cloak.RANDOM_VALUE
        self.name = "IPv6 Hoppers"
        self.description = "A covert channel using the hop limit in IPv6 packets to transmit messages."
        self.ip_dst = ip_dst
        self.ip_src = ip_src
        self.EOT_hl = EOT_hl
        self.read_data = []

    def ingest(self, data):
        #Ingests the data to send cov3rtly
        if isinstance(data, str):
            self.data = [ord(i) for i in data]

    def send_EOT(self):
        #Sends the EOT packet
        pkt = IPv6(src = 'fe80::1461:beca:7ad:3167', dst = 'ff02::1:ffad:317')
        pkt.hlim = self.EOT_hl
        send(pkt)

    def send_packet(self, var_hl):
        pkt = IPv6(src = 'fe80::1461:beca:7ad:3167', dst = 'ff02::1:ffad:317')
        pkt.hlim = var_hl + self.EOT_hl
        send(pkt)

    def send_packets(self, packetDelay = None, delimitDelay = None, endDelay = None):
        print("Sending data:")
        print(self.data)
        
        pkt = IPv6(src = 'fe80::1461:beca:7ad:3167', dst = 'ff02::1:ffad:317')
        pkt.hlim = self.EOT_hl
        
        for item in self.data:
            var_hl = item
            self.send_packet(var_hl)
            if (isinstance(packetDelay, int) or isinstance(packetDelay, float)):
                sleep(packetDelay)
       
        if (isinstance(endDelay, int) or isinstance(endDelay, float)):
            sleep(endDelay)
        self.send_EOT()
        return True

    def packet_handler(self, pkt):
        #Determines what packets we accept when choosing data
        if (pkt.haslayer(IPv6)):
            if(pkt.dst == self.ip_dst and pkt.src == self.ip_src):
                self.read_data.append(pkt.hlim)

    def recv_EOT(self,pkt):
        #Looks for EOT packet to signify end of transmission
        if (pkt.haslayer(IPv6)): 
            if (pkt.dst == self.ip_dst and pkt.hlim == self.EOT_hl):  
                return True
        return False

    def recv_packets(self, timeout = None, max_count = None, iface = None, in_file = None, out_file = None):
        #Sniffs and receives packets transmitted by IPv6Hoppers Cloak
        self.read_data = []
        if max_count:
            sniff(timeout = timeout, count = max_count, iface = iface, offline = in_file, store = out_file, stop_filter = self.recv_EOT, prn = self.packet_handler)
        else:
            sniff(timeout = timeout, iface = iface, offline = in_file, store = out_file, stop_filter = self.recv_EOT, prn = self.packet_handler)

        # When an EOT packet is received, the message is decoded for the user
        print("Sniffing has ended, EOT received")
        decoded_string = ''
        
        for item in self.read_data[:-1]:
            decoded_string += chr(item - self.EOT_hl)
            print("Decoded Message: {}".format(decoded_string))

        return decoded_string

    # Getters and Setters

    # Getter for "ip_dst"
    @property
    def ip_dst(self):
        return self._ip_dst

    # Setter for "ip_dst"
    @ip_dst.setter
    def ip_dst(self,ip_dst):
        # Ensure valid type:str
        if isinstance(ip_dst, str):
            # Ensure valid IP format
            if search(self.IPv6_REGEX, ip_dst):
                self._ip_dst = ip_dst
            else:
                error("Invalid IP address provided: {}".format(ip_dst))
        else:
            error("'ip_dst' must be of type 'str'")

    # Getter for "ip_src"
    @property
    def ip_src(self):
        return self._ip_src

    # Setter for "ip_src"
    @ip_dst.setter
    def ip_src(self,ip_src):
        # Ensure valid type:str
        if isinstance(ip_src, str):
            # Ensure valid IP format
            if search(self.IPv6_REGEX, ip_src):
                self._ip_src = ip_src
            else:
                error("Invalid IP address provided: {}".format(ip_src))
        else:
            error("'ip_src' must be of type 'str'")        

    # Getter for "EOT_hl"
    @property
    def EOT_hl(self):
        return self._EOT_hl

    # Setter for "EOT_hl"
    @EOT_hl.setter
    def EOT_hl(self, EOT_hl):
        if ( isinstance(EOT_hl, int)):
            if (EOT_hl > 64 and EOT_hl < 127):
                self._EOT_hl = EOT_hl
            else:
                error("'EOT_hl' must be between 64 and 127")
        else:
            error("'EOT_hl' must be of type  'int'")
