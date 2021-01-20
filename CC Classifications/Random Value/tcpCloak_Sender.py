from scapy.all import *

IP_DST = "10.0.0.4"

# Get user input
user_input = input("Enter your secret phrase: ")

# Creating packet
p = IP(dst=IP_DST)/TCP()

# Iterate through secret message and send each as a deciaml value
for i in user_input:
    num = ord(i)
    p["TCP"].seq = num
    send(p)

p["IP"].flags = 0x06
send(p)
