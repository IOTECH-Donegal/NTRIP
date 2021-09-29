import sys
import time
import datetime
import serial

# Utilities used by all RTCM tools
from rtcm.RTCMParser import RTCMParser
myRTCM = RTCMParser()

# Create a Serial port class
from SerialSender import SerialHandler
mySerialPort = SerialHandler()

# Set the mount point values
myRTCM.ntrip_server = 'rtk2go.com'
myRTCM.ntrip_port = 2101
myRTCM.ntrip_mount_point = '/Umricam'

try:
    # Create the mount point web query
    myRTCM.create_mount_point()
    # Main loop
    while True:
        print('\n')
        print(f'Running web query at: {datetime.datetime.now()}')
        if myRTCM.connect():
            myRTCM.rtcm_parser()
            mySerialPort.write_buffer = myRTCM.response_bytes
            mySerialPort.write_bytes()
        time.sleep(5)
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
    print("Exiting")
    mySerialPort.close()
    exit(0)