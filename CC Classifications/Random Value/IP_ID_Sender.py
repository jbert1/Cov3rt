from scapy.all import *

#IP Destination Default
IP_DST = "10.10.10.10"


#Collect the phrase the user wants to send
secret_phrase = input("Enter your Secret Phrase: ")

#Retreive ASCII value for each character in secret phrase
secret_phrase_dec = [ord(i) for i in secret_phrase]

p = IP(dst = IP_DST)

ls(p)
#For each character ...
for character in secret_phrase_dec:
    p.id = character
    send(p)

p.id = 42069
send(p)