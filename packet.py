import socket, sys, time, zlib, string
import struct
import binascii
import random

class Packet:
    TCP_LENGTH = 20 # 20 Bytes => minimum size
    UDP_LENGTH = 16 # 16 Bytes => minimum size
    IP_PROTOCOL = 6 # 6 => TCP // 17 => UDP
    TOTAL_LENGTH = 40 # 40 => TCP / 28 => UDP

    def __init__(self, src_ip,dst_ip, packet_type = 'tcp'):
        self.SRC_IP = socket.inet_aton(src_ip)
        self.DST_IP = socket.inet_aton(dst_ip)
        if packet_type == 'tcp':
            self.IP_PROTOCOL = 6
            self.TOTAL_LENGTH = 40
        elif packet_type == 'udp':
            self.IP_PROTOCOL = 17
            self.TOTAL_LENGTH = 28
        else:
            self.TOTAL_LENGTH = 0

    # checksum calculator 
    def checksum(self,data):
        countTo = (len(data) // 2) * 2
        x = 0
        count = 0
        while count < countTo:
            x += data[count] + (data[count+1] << 8)
            count += 2
        
        if countTo < len(data):
            x+= data[len(data)-1]

        x &= 0xffffffff
        
        x = (x >> 16) + (x & 0xffff)
        x += (x >> 16)
        checksum = ~x & 0xffff
        checksum = socket.htons(checksum)
        return checksum
        
    # generate random hex 
    def generate_random(self,length):
        pick_from = "0123456789abcdef"
        rand = ''
        for i in range(0,length):
            rand += random.choice(pick_from)
        rand = binascii.unhexlify(rand)
        return rand

    # udp header
    def udp_header(self):
        ## fields of udp header
        src_port = 5000 #random.randint(1024,65535)
        dst_port = 80
        length = 8 # 8 bytes
        checksum = 0
        ## encapsulate the packet with 0 checksum
        udp_h = struct.pack('!4H',src_port,dst_port,length,checksum)

        ## add pseudo ip headers
        pseudo_ip = struct.pack('!H4s4sH', self.IP_PROTOCOL,self.SRC_IP, self.DST_IP,self.UDP_LENGTH)
        #calculate the UDP checksum
        real_checksum = self.checksum(pseudo_ip+udp_h)
        ## encapsulate the packet!
        udp_h = struct.pack('!4H',src_port,dst_port,length,real_checksum)
        return udp_h

    # tcp header
    def tcp_header(self, 
                    src_port=12345,
                    dst_port=80,
                    seq_number=0,
                    ack_number = 0,
                    data_offset='0101000000000010',
                    window_size=28944,
                    urg_pointer=0
                ):
        
        data_offset =  int(data_offset,2) # SYN (check tcp headers)
        ## encapsulate the packet with 0 checksum
        tcp_h = struct.pack('!6H',src_port,dst_port,seq_number,ack_number, data_offset,window_size)
        ## add pseudo ip headers
        pseudo_ip = struct.pack('!H4s4sH', self.IP_PROTOCOL,self.SRC_IP, self.DST_IP,self.TCP_LENGTH)
        #calculate the TCP checksum
        real_checksum = self.checksum(pseudo_ip+tcp_h)
        ## encapsulate the packet!  
        tcp_h = struct.pack('!2H2L4H',src_port,dst_port,seq_number,ack_number, data_offset,window_size,real_checksum,urg_pointer)
        return tcp_h

    # ip header
    def ip_header(self, 
                    ip_version='0100',
                    ip_ihl='0101',
                    type_of_service=0,
                    identification=43981,
                    flags_and_fragement_offset='0000000000000000',
                    ttl=64,
                ):
        
        ver_ihl = int(ip_version+ip_ihl , 2) # version and IHL
        flags_and_fragement_offset = int(flags_and_fragement_offset,2)
        pkt = struct.pack('!BBHHHBB4s4s',ver_ihl,type_of_service,self.TOTAL_LENGTH,identification,flags_and_fragement_offset,ttl,self.IP_PROTOCOL,self.SRC_IP,self.DST_IP)
        checksum = self.checksum(pkt)
        pkt = struct.pack('!BBHHHBBH4s4s',ver_ihl,type_of_service,self.TOTAL_LENGTH,identification,flags_and_fragement_offset,ttl,self.IP_PROTOCOL,checksum,self.SRC_IP,self.DST_IP)
        return pkt

    # ethernet header
    def eth_header(self):
        ethernet = b'\xFF\xFF\xFF\xFF\xFF\xFF' # MAC Address Dest
        ethernet += self.generate_random(12)   # MAC Address Source
        ethernet += b'\x08\x00'                # Protocol-Type: IPv4
        return ethernet