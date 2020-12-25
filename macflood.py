import socket, time
from packet import Packet

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
pkt = Packet(src_ip='192.168.1.150', dst_ip='192.168.1.50',packet_type=None)

#layer 2 / layer 3
packet = pkt.eth_header() + pkt.ip_header()

interface = input('select interface ')
s.bind((interface, 0))

number_of_packets = int(input('number of packets '))

for i in range(number_of_packets):
    s.send(packet)