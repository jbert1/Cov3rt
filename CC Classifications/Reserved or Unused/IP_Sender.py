from scapy.all import *

IP_DST = "10.0.0.4"

# Get user input
user_input = input("Enter your secret phrase: ")

# Convert user input to binary
bin_user_input = ''.join(format(ord(i), 'b').zfill(8) for i in user_input)

# Create IP packet
p = IP(dst=IP_DST)

# Loop through binary version of user input and send values through the reserved field of IP
for i in bin_user_input:
    if i == '0':
        p["IP"].flags = 0x00
        send(p)

    if i == '1':
        p["IP"].flags = 0x04
        send(p)

# Signal end of transmission
p["IP"].flags = 0x06
send(p)


