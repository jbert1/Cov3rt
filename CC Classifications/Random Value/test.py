from scapy.all import *


p = IPv6(src = 'fe80::1461:beca:7ad:3167', dst = 'fe80::1461:beca:7ad:3167')

ls(p)
print('\n')
p.hlim = 12
ls(p)
send(p)