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

# Utilities used by all RTCM tools
from rtcm.RTCMParser import RTCMParser
myRTCM = RTCMParser()

ntrip_server = 'rtk2go.com'
ntrip_port = 2101
ntrip_mountpoint = '/Umricam'
ntrip_mount_point_str = "GET %s HTTP/1.0\r\n" % (ntrip_mountpoint)
ntrip_mount_point_str +="User-Agent: IOTECH NTRIP Client" + "\r\n"
ntrip_mount_point_str +="Accept: */*" + "\r\n"
ntrip_mount_point_str +="Connection: close" + "\r\n" + "\r\n"
ntrip_mount_point_bytes = bytes(ntrip_mount_point_str, 'UTF-8')
debug = 1


def mountpoint():
    print('Mountpoint Web Service Query:')
    if debug == 1:
        print(ntrip_mount_point_str)
        print_bytes = ":".join("{:02x}".format(ord(c)) for c in ntrip_mount_point_str)

        print('Mountpoint Web Service Query in Hex:')
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
        # At present, payload is c. 6KB, set buffer bigger
        response_bytes = ntrip_socket.recv(8192)
        # Extract the header from the byte string, do not use UTF-8, it fails on 0xd3
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
                # The first xd3 byte should be found after the header, CR and LF
                start_pointer = header_length + 2
                # Check for a xd3
                if response_bytes[start_pointer] == 211:
                    myRTCM.rtcm_parser(response_bytes)


try:
    mountpoint()
    go()
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError as err:
    print("Value Error error: {0}".format(err))
except KeyboardInterrupt:
    print("\n" + "Caught keyboard interrupt, exiting")
    exit(0)
except:
    print("Unexpected error:", sys.exc_info()[0])
finally:
    print("Exiting Main Thread")
    exit(0)