from scapy.all import *

starting_hl = 68

# Collects user input to determine content of message to send over the covert channel
secret_phrase = input("Enter your Secret Phrase:")

# Retrieves ASCII Value for every character in secret phrase
secret_phrase_dec = [ord(i) for i in secret_phrase]

# print(secret_phrase_dec) DEBUG

# Creates an IPv6 Packet 
p = IPv6(src = 'fe80::1461:beca:7ad:3167', dst = 'ff02::1:ffad:317')

# Sets Hop Limit to transmit at start and end of phrase transmission
p.hlim = starting_hl

# ls(p) DEBUG

# Sends packet
send(p)

# For each character ...
for c in secret_phrase_dec:
    # Set Hop Limit to ASCII character value + initial hop limit
    p.hlim = c + starting_hl 
    

    # print(c) DEBUG
    # ls(p) DEBUG
    
    # Send the packet
    send(p)

# Sets Hop Limit to transmit at start and end of phrase transmission
p.hlim = starting_hl

# ls(p) DEBUG

send(p)