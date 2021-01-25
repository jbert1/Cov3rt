from scapy.sendrecv import send, sniff
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP

from logging import error
from re import search
from time import sleep

from Cloak import Cloak

'''

VARIABLES REQUIRED
IPv6 Source (ip_src)
IPv6 Destination (ip_dst)
EOT Hop Limit (Will be EOT_hl) (Recommended to be set between 64 and 128)

'''

class IPv6Hoppers(Cloak):
    

    def __init__(self, ip_dst = "ff02::1:ffad:317"):
        self.description = "A covert channel using the hop limit in IPv6 packets to transmit messages."
        self.name = "IPv6Hoppers"
        self.ip_dst = ip_dst
        self.ip_src = ip_src
        self.read_data = []
        self.EOT_hl = EOT_hl

    def ingest(self, data):
        #Ingests the data to send cov3rtly
        if isinstance(data, str):
            self.data = [ord(i) for i in data]

    def send_EOT(self):
        #Sends the EOT packet
        pkt = IPv6(src = 'fe80::1461:beca:7ad:3167', dst = 'ff02::1:ffad:317')
        pkt.hlim = EOT_hl
        send(pkt)

    def send_packet(self, data):
        pass

    def send_packets(self, packetDelay = None, delimitDelay = None, endDelay = None):
