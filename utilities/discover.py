#! /usr/bin/env python
import socket
import json
import sys
import time

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
answersocket.settimeout(3)

answers=[]
knownbotips=[]
print "Searching for a makerbot..."
for _ in range(3):
    broadcastsocket.sendto(discover_request, (host,target_port),)
    try:
        data, fromaddr = answersocket.recvfrom(1024)
        if fromaddr not in knownbotips:
            knownbotips.append(fromaddr)
            print "Got a reply from ",fromaddr
            answers.append(data)
        else:
            continue
    except:
        continue
    time.sleep(1)

if len(answers)==0:
    print "No bots found :("
    sys.exit(1)

for data in answers:
    infodic=json.loads(data)
    print ""
    print "Machine Name: ",infodic['machine_name']
    print "IP Address: ",infodic['ip']
    print "Serial: ",infodic['iserial']


