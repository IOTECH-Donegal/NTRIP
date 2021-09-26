""""
Wireshark capture of working str2str was:
GET /Umricam HTTP/1.0\r\n
User-Agent: NTRIP
Accept: */*\r\n
Connection: close\r\n
\r\n
"""

import socket
import base64

ntrip_server = 'rtk2go.com'
ntrip_port = 2101
ntrip_user_str = 'john.oraw@hotmail.com'
ntrip_caster = ''
ntrip_useragent = 'IOTECH NTRIP Client'
ntrip_mountpoint = 'Umricam'
ntrip_mount_point_string = "Ntrip-Version: Ntrip/2.0\r\n"
ntrip_user = base64.b64encode(bytes(ntrip_user_str, 'utf-8')).decode("utf-8")
ntrip_mount_point_str = "GET %s HTTP/1.1\r\nUser-Agent: %s\r\nAuthorization: Basic %s\r\n" % (ntrip_mountpoint, ntrip_useragent, ntrip_user)

host_string = "Host: %s:%i\r\n" % (ntrip_caster,ntrip_port)
mount_point = "Ntrip-Version: Ntrip/2.0\r\n"
ntrip_mount_point_str += host_string
ntrip_mount_point_str += mount_point




debug = 1

def mountpoint():
    if debug == 1:
        print(f'NTRIP server: {ntrip_server}:{ntrip_port}')
        print(f'NTRIP mount point: {ntrip_mountpoint}')
        print(f'NTRIP user: {ntrip_user_str} in base64= {ntrip_user}')
        print(f'NTRIP mount point HTTP string {ntrip_mount_point_str}')




#socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.settimeout(10)
#socket.sendall(etMountPointBytes())

mountpoint()