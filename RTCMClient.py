import sys
import time
import datetime

# Utilities used by all RTCM tools
from rtcm.RTCMParser import RTCMParser
myRTCM = RTCMParser()

# Set the mount point values
myRTCM.ntrip_server = 'rtk2go.com'
myRTCM.ntrip_port = 2101
myRTCM.ntrip_mount_point = '/Umricam'

try:
    # Create the mount point web query
    myRTCM.create_mount_point()
    # Main loop
    while True:
        print(f'Running web query at: {datetime.datetime.now()} \n')
        if myRTCM.run():
            myRTCM.rtcm_parser()
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
    print("Exiting Main Thread")
    exit(0)