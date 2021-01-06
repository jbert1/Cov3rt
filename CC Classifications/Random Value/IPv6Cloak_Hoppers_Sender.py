from scapy.all import *

IP_DST = "1234:5678:9001:1337:ABCD:0000:FACE:AAAA"

# Collects user input to determine content of message to send over the covert channel.
secret_phrase = input("Enter your Secret Phrase:")

secret_phrase_bin = ''.join((format(ord(i), 'b').zfill(8) for i in secret_phrase))


p = IPv6()
p
