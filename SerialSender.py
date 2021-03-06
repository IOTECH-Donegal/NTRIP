import serial


class SerialHandler():
    # Constructor
    def __init__(self):
        # Switch this on for verbose processing
        self.debug = 0
        # initialize properties, set from calling programme
        self.write_buffer = b"\xd3"
        # Set up the serial port
        self.SerialPort = serial.Serial(
            # For Windows
            port='COM10',
            # For RPi
            # port='/dev/ttySC1',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=2
        )

    def run(self):
        """ Do any initilization after port is opened"""
        self.SerialPort.flushInput()

    def write_bytes(self):
        """ Write bytes from a class level buffer to the serial port"""
        self.SerialPort.write(self.write_buffer)

    def close(self):
        """ Close the port at the end of a session"""
        self.SerialPort.close()

