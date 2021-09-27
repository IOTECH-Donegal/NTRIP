""""
Wireshark capture of working str2str was:
GET /Umricam HTTP/1.0\r\n
User-Agent: NTRIP
Accept: */*\r\n
Connection: close\r\n
\r\n
"""

import sys
import socket
import time
import textwrap
import base64

ntrip_server = 'rtk2go.com'
ntrip_port = 2101
ntrip_mountpoint = '/Umricam'
ntrip_mount_point_str = "GET %s HTTP/1.0\r\n" % (ntrip_mountpoint)
ntrip_mount_point_str +="User-Agent: IOTECH NTRIP Client" + "\r\n"
ntrip_mount_point_str +="Accept: */*" + "\r\n"
ntrip_mount_point_str +="Connection: close" + "\r\n" + "\r\n"
ntrip_mount_point_bytes = bytes(ntrip_mount_point_str, 'UTF-8')
debug = 1


def convert_int_to_byte(int):
    return int.to_bytes(1, 'little', signed=False)


def mountpoint():
    if debug == 1:
        print(ntrip_mount_point_str)
        print_bytes = ":".join("{:02x}".format(ord(c)) for c in ntrip_mount_point_str)
        print('\n'.join(textwrap.wrap(print_bytes, 48)))




def go():

    line = ''
    header_length = 0

    while True:
        # Set up for communications
        ntrip_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ntrip_socket.connect((ntrip_server, ntrip_port))
        # Send the query
        ntrip_socket.sendall(ntrip_mount_point_bytes)
        # Get the response
        time.sleep(1)
        response_bytes = ntrip_socket.recv(4096)
        # Extract the header from the byte string
        response_string = response_bytes.decode("latin-1").split("\r\n")
        # Check to see if valid
        for line in response_string:
            if line.find("401 Unauthorized") >= 0:
                sys.stderr.write("Unauthorized\n")
                sys.exit(1)
            elif line.find("404 Not Found") >= 0:
                sys.stderr.write("No Mount Point\n")
                sys.exit(2)
            elif line.find("ICY 200 OK") >= 0:
                print(line)
                header_length = len(line)

        # Remove the CR LF at the and of the header, payload is an integer array
        payload = bytearray(response_bytes[header_length + 2:])
        print(type(payload))




mountpoint()
go()