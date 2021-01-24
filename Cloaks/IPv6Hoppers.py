from scapy.sendrecv import send, sniff
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP

from logging import error
from re import search
from time import sleep

from Cloak import Cloak


class IPv6Hoppers(Cloak):
    pass