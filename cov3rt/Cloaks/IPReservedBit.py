from scapy.all import *

from logging import error
from re import search
from time import sleep

from cov3rt.Cloaks.Cloak import Cloak

class IPReservedBit(Cloak):
    
    def __init__(self, ip_dst = "8.8.8.8"):
        self.classification = Cloak.RESERVED_UNUSED
        self.name = "IP Reserved Bit"
        self.description = "A cloak based on modulating the reserved bit in the IP header field."
        self.ip_dst = ip_dst
        self.read_data = ""

    def ingest(self,data):
        
        if isinstance(data, str):
            self.data = ''.join(format(ord(i),'b').zfill(8) for i in data)
        
        else:
            error("'data' must be of type 'str'")

    def send_EOT(self):
        
        pkt = IP(dst=self.ip_dst, flags=0x06)
        send(pkt, verbose=False)

    def send_packet(self, databit):
        
        if databit == '0':
            pkt = IP(dst=self.ip_dst)
            pkt["IP"].flags = 0x00
            send(pkt, verbose=False)

        elif databit == '1':
            pkt = IP(dst=self.ip_dst)
            pkt["IP"].flags = 0x04
            send(pkt, verbose=False)


    def send_packets(self, packetDelay = None, delimitDelay = None, endDelay = None):
        
        for item in self.data:
            self.send_packet(item)

            if(isinstance(packetDelay, int) or isinstance(packetDelay, float)):
                sleep(packetDelay)
        
        if(isinstance(endDelay, int) or isinstance(endDelay, float)):
            sleep(endDelay)

        self.send_EOT()
        return True
            

    def packet_handler(self,pkt):

        if pkt.haslayer(IP):
            if pkt["IP"].dst == self.ip_dst:
                if pkt["IP"].flags == 0x00:
                    self.read_data += '0'
                elif pkt["IP"].flags == 0x04:
                    self.read_data += '1'

    def recv_EOT(self,pkt):
        
        if pkt.haslayer(IP):
            if (pkt["IP"].dst == self.ip_dst and pkt["IP"].flags == 0x06):
                return True
        return False

    def recv_packets(self, timeout = None, max_count = None, iface = None, in_file = None, out_file = None):

        self.read_data = ""

        if max_count:
            sniff(timeout = timeout, count = max_count, iface = iface, offline = in_file, store = out_file, stop_filter = self.recv_EOT, prn = self.packet_handler)
        else:
            sniff(timeout = timeout, iface = iface, offline = in_file, store = out_file, stop_filter = self.recv_EOT, prn = self.packet_handler)

        output_string = ""

        for i in range(0,len(self.read_data),8):

            char = "0b{}".format(self.read_data[i:i+8])

            output_string = output_string + chr(int(char,2))

        return output_string
        
    # Getters and setters
    # IDK which ones to make getters and setters
