from scapy.all import *

#End of Transmission Hop Limit (Recommended to be between 64 and 128)
eot_hl = 68

# Collects user input to determine content of message to send over the covert channel
secret_phrase = input("Enter your Secret Phrase:")

# Retrieves ASCII Value for every character in secret phrase
secret_phrase_dec = [ord(i) for i in secret_phrase]

# print(secret_phrase_dec) DEBUG

# Creates an IPv6 Packet 
p = IPv6(dst = 'ff02::1:ffad:317')

# Sets Hop Limit to transmit at end of phrase transmission
p.hlim = eot_hl

# ls(p) DEBUG


# For each character ...
for c in secret_phrase_dec:
    # Set Hop Limit to ASCII character value + initial hop limit
    p.hlim = c + eot_hl 
    

    # print(c) DEBUG
    # ls(p) DEBUG
    
    # Send the packet
    send(p)

# Sets Hop Limit to transmit at start and end of phrase transmission
p.hlim = eot_hl

# ls(p) DEBUG

# Send the packet
send(p)