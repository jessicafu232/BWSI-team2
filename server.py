# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:43:54 2019

@author: RA23103
"""

import logging
import socket
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(20)

# Bind the socket to the port
try:
    server_address = ('localhost', 10000)
    logger.info('Starting up on {0} port {1}'.format(server_address[0], server_address[1]))
    sock.bind(server_address)
except Exception as err:
    logger.info('{0} {1}'.format(err.message, err.args))

start_time = time.time()
elapsed_time = 0
max_time = 60
while elapsed_time < max_time:
    logger.info('Waiting to receive message...')
    try:
        data, address = sock.recvfrom(4096)
    except:
        logger.error('Timed out!')
        break
    data = data.decode('utf-8')
    
    logger.info('Received {0} bytes from {1}'.format(len(data), address))
    logger.info(data)
    
    if data:
        data = data.encode('utf-8')
        sent = sock.sendto(data, address)
        logger.info('Sent {0} bytes back to {1}'.format(sent, address))
        
    elapsed_time = time.time() - start_time
        
logger.info('Closing socket')
sock.close()
