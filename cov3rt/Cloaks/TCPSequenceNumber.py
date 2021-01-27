from scapy.sendrecv import send, sniff
from scapy.layers.inet import IP, TCP

from logging import error
from time import sleep

from cov3rt.Cloaks.Cloak import Cloak

class TCPSequenceNumber(Cloak):

    # Classification, name, and description
    classification = Cloak.RANDOM_VALUE
    name = "TCP Sequence Number"
    description = "A cloak based on changing the TCP sequence number ASCII values."
    
    def __init__(self, ip_dst="8.8.8.8"):
        self.ip_dst = ip_dst
        self.read_data = ""

    def ingest(self,data):

        if isinstance(data,str):
            self.data = [ord(i) for i in data]

        else:
            error("'data' must be of type 'str'")

    def send_EOT(self):

        pkt = IP(dst=self.ip_dst, flags=0x06)
        send(pkt, verbose=False)

    def send_packet(self, num):
        
        pkt = IP(dst=self.ip_dst)/TCP(seq=num)
        send(pkt, verbose=False)

    def send_packets(self, packetDelay = None, delimitDelay = None, endDelay = None):
        
        for num in self.data:
            self.send_packet(num)

            if(isinstance(packetDelay, int) or isinstance(packetDelay, float)):
                sleep(packetDelay)

        if(isinstance(endDelay, int) or isinstance(endDelay, float)):
            sleep(endDelay)

        self.send_EOT()
        return True

    def packet_handler(self,pkt):
        
        if pkt.haslayer(TCP):
            if pkt["IP"].dst == self.ip_dst and pkt["IP"].flags != 0x06:
                self.read_data += chr(pkt["TCP"].seq)

    def recv_EOT(self,pkt):

        if pkt.haslayer(IP):
            if pkt["IP"].dst == self.ip_dst and pkt["IP"].flags == 0x06:
                return True
        return False

    def recv_packets(self, timeout = None, max_count = None, iface = None, in_file = None, out_file = None):

        self.read_data = ""

        if max_count:
            sniff(timeout = timeout, count = max_count, iface = iface, offline = in_file, store = out_file, stop_filter = self.recv_EOT, prn = self.packet_handler)
        else:
            sniff(timeout = timeout, iface = iface, offline = in_file, store = out_file, stop_filter = self.recv_EOT, prn = self.packet_handler)

        return self.read_data

    # Getters and Setters
    # IDK which ones to put here


