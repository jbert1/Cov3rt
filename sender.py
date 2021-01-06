from scapy.all import *
import stream_schema as s

# Get user input
user_input = input("Enter your secret phrase: ")

init = s.Example()
init.ip_dst = "10.0.0.4"
init.ingest(user_input)

for i in init.data:
    init.update(i)
    send(init.packet)

init.EOF()
send(init.packet)
