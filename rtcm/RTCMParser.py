
import textwrap




class RTCMParser():
    # Constructor
    def __init__(self):

        # Switch this on for verbose processing
        self.debug = 1

    def rtcm_parser(self, response_bytes):
        length_of_buffer = len(response_bytes)
        print(f'Buffer = {length_of_buffer}')
        response_string = response_bytes.decode("latin-1").split("\r\n")
        print_bytes = ":".join("{:02x}".format(ord(c)) for c in response_string[1])
        print('Mountpoint Web Service Query in Hex:')
        print('\n'.join(textwrap.wrap(print_bytes, 48)))
        # Get the legth of the header
        header_length = len(response_string[0])
        print(f'Header length is {header_length}')
        # The first xd3 byte should be found after the header, CR and LF
        rtcm_payloads = response_bytes[header_length + 2:]
        length_of_payloads = len(rtcm_payloads)
        # SOF should be xd3 or int=211
        byte1 = rtcm_payloads[0:1]
        # Set the pointers
        start_pointer = 0
        end_pointer = 0

        while end_pointer + 3 < length_of_payloads:
            # Extract one message at a time from the stream
            if byte1 == b"\xd3":
                byte2 = rtcm_payloads[start_pointer + 1:start_pointer +2]
                byte3 = rtcm_payloads[start_pointer + 2:start_pointer +3]
                byte2and3 = rtcm_payloads[start_pointer +1:start_pointer +3]
                # The first 6 bits are reserved, but always zero, so convert the first two bytes directly to int
                length_of_payload = int.from_bytes(byte2and3, "big", signed=False)
                # The end of this message is the message length + 3 byte CRC
                end_pointer = start_pointer + length_of_payload + 3
                print(f'Length = {length_of_payload} derived from {byte2.hex()} and {byte3.hex()}')
                this_message = rtcm_payloads[start_pointer:start_pointer + end_pointer]
                # Locate the message ID and convert it to an INT, its 12 bits of 16 so divide by 16
                byte4 = rtcm_payloads[start_pointer +3:start_pointer +4]
                byte5 = rtcm_payloads[start_pointer +4:start_pointer +5]
                message_id_int = int.from_bytes(byte4+byte5, "big") / 16
                print(f'RTCM3: Received {str(message_id_int)} derived from {byte4.hex()} and {byte5.hex()}')
                print('')
            start_pointer = end_pointer +3
            byte1 = rtcm_payloads[start_pointer:start_pointer + 1]
            print(end_pointer, length_of_payloads)


