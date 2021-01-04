from scapy.all import *

# Get user input
user_input = input("Enter your secret phrase: ")

# Convert user input ot binary
bin_user_input = ''.join(format(ord(i), 'b') for i in user_input)

# Create IP packet
p = IP(dst='10.0.0.4')

# Loop through binary version of user input and send values through the reserved field of IP
for i in bin_user_input:
    if i == '0':
        #print("This is a 0")
        p['IP'].flags = 0x00
        send(p)

    if i == '1':
        #print("This is a 1")
        p['IP'].flags = 'evil'
        send(p)

# Send the user input as raw data at the end of an IP packet
p = p/user_input
send(p)


