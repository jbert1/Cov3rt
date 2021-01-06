from scapy.all import *

IP_DST = "1234:5678:9001:1337:ABCD:0000:FACE:AAAA"

# Collects user input to determine content of message to send over the covert channel.
secret_phrase = input("Enter your Secret Phrase:")

secret_phrase_dec = [ord(i) for i in secret_phrase]

print(secret_phrase_dec)

ls(IPv6)
p = IPv6(src = 'fe80::1461:beca:7ad:3167', dst = 'fe80::1461:beca:7ad:3167')

p.hlim = 69
send(p)

for c in secret_phrase_dec:
    p.hlim = c
    print(c)
    ls(IPv6)
    send(p)

p.hlim = 69
send(p)