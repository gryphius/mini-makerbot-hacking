#! /usr/bin/env python
import socket
import json
host='255.255.255.255'

target_port = 12307
listen_port = 12308
source_port = 12309

broadcastsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcastsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcastsocket.bind(('0.0.0.0', source_port))

answersocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
discover_request='{"command": "broadcast"}'
answersocket.bind(('0.0.0.0', listen_port))

print "Searching for a makerbot..."
broadcastsocket.sendto(discover_request, (host,target_port),)
answersocket.settimeout(10)
try:
    data, fromaddr = answersocket.recvfrom(1024)
    print "Got a reply from ",fromaddr
except:
    print "No bot found :("

infodic=json.loads(data)

print ""
print "Machine Name: ",infodic['machine_name']
print "IP Address: ",infodic['ip']
print "Serial: ",infodic['iserial']


