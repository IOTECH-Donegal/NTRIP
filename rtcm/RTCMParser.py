import textwrap
import socket
import time
import sys


class RTCMParser():
    # Constructor
    def __init__(self):
        # Switch this on for verbose processing
        self.debug = 0
        # initialize properties, set from calling programme
        self.response_bytes = b"\xd3"
        self.ntrip_mount_point_str = ''
        self.ntrip_server = ''
        self.ntrip_port = 0
        self.ntrip_mount_point = ''
        self.ntrip_mount_point_bytes = b"\x00"

    def create_mount_point(self):
        self.ntrip_mount_point_str = "GET %s HTTP/1.0\r\n" % self.ntrip_mount_point
        self.ntrip_mount_point_str += "User-Agent: IOTECH NTRIP Client" + "\r\n"
        self.ntrip_mount_point_str += "Accept: */*" + "\r\n"
        self.ntrip_mount_point_str += "Connection: close" + "\r\n" + "\r\n"
        self.ntrip_mount_point_bytes = bytes(self.ntrip_mount_point_str, 'UTF-8')

        if self.debug:
            print_bytes = ":".join("{:02x}".format(ord(c)) for c in self.ntrip_mount_point_str)
            print('Mount point Web Service Query in Hex:')
            print('\n'.join(textwrap.wrap(print_bytes, 48)))
            print('\n')

    def run(self):
        # Set up for communications
        ntrip_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ntrip_socket.connect((self.ntrip_server, self.ntrip_port))
        # Send the query
        ntrip_socket.sendall(self.ntrip_mount_point_bytes)
        # Get the response
        time.sleep(1)
        # At present, payload is c. 6KB, set buffer bigger
        self.response_bytes = ntrip_socket.recv(8192)
        # Extract the header from the byte string, do not use UTF-8, it fails on 0xd3
        response_string = self.response_bytes.decode("latin-1").split("\r\n")
        # Check to see if valid
        for line in response_string:
            if line.find("ICY 200 OK") >= 0:
                header_length = len(line)
                # The first xd3 byte should be found after the header, CR and LF
                start_pointer = header_length + 2
                # Check for a xd3 = int 211
                if self.response_bytes[start_pointer] == 211:
                    return True
                else:
                    return False
            elif line.find("401 Unauthorized") >= 0:
                sys.stderr.write("Unauthorized\n")
                sys.exit(1)
            elif line.find("404 Not Found") >= 0:
                sys.stderr.write("No Mount Point\n")
                sys.exit(2)
            else:
                print(line)

    def rtcm_parser(self):
        length_of_buffer = len(self.response_bytes)
        response_string = self.response_bytes.decode("latin-1").split("\r\n")
        # Get the length of the header
        header_length = len(response_string[0])
        # The first xd3 byte should be found after the header, CR and LF
        rtcm_payloads = self.response_bytes[header_length + 2:]
        length_of_payloads = len(rtcm_payloads)
        # SOF should be xd3 or int=211
        byte1 = rtcm_payloads[0:1]
        # Set the pointers
        start_pointer = 0
        end_pointer = 0

        while end_pointer + 3 < length_of_payloads:
            # Extract one message at a time from the stream
            if byte1 == b"\xd3":
                byte2 = rtcm_payloads[start_pointer + 1:start_pointer + 2]
                byte3 = rtcm_payloads[start_pointer + 2:start_pointer + 3]
                byte2and3 = rtcm_payloads[start_pointer + 1:start_pointer + 3]
                # The first 6 bits are reserved, but always zero, so convert the first two bytes directly to int
                length_of_payload = int.from_bytes(byte2and3, "big", signed=False)
                # The end of this message is the message length + 3 byte CRC
                end_pointer = start_pointer + length_of_payload + 3
                this_message = rtcm_payloads[start_pointer:start_pointer + end_pointer]
                # Locate the message ID and convert it to an INT, its 12 bits of 16 so divide by 16
                byte4 = rtcm_payloads[start_pointer + 3:start_pointer + 4]
                byte5 = rtcm_payloads[start_pointer + 4:start_pointer + 5]
                message_id_int = int.from_bytes(byte4 + byte5, "big") / 16
                if self.debug:
                    print(f'Length = {length_of_payload} derived from {byte2.hex()} and {byte3.hex()}')

                print(f'RTCM3: Received {str(message_id_int)} derived from {byte4.hex()} and {byte5.hex()}')
                print('')
            # Move the start pointer to the end of the message, plus the CRC
            start_pointer = end_pointer + 3
            # Read byte1 to get started again
            byte1 = rtcm_payloads[start_pointer:start_pointer + 1]
