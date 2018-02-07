# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 15:58:08 2016

@author: Justin Fletcher
@title: 
"""

import MalmoPython
import os
import sys
import time
import numpy
import platform
import socket
import subprocess

from multiprocessing import Process
from multiprocessing import Pool
from multiprocessing import Queue

from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE


sys.path.insert(0, 'C:/Malmo/malmo_net/')
import malmo_exoself as me


# Print the current working directory.
#print os.getcwd()

# flush print output immediately.
#sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


def get_mission_xml(num_agents=1):

    xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

        <About>
            <Summary>Survival</Summary>
        </About>
        <ModSettings>
            <MsPerTick> 50 </MsPerTick>
            <PrioritiseOffscreenRendering>false</PrioritiseOffscreenRendering>
        </ModSettings>

        <ServerSection>
            <ServerInitialConditions>
                <AllowSpawning>true</AllowSpawning>
            </ServerInitialConditions>
            <ServerHandlers>
                <DefaultWorldGenerator/>
            </ServerHandlers>
        </ServerSection>'''

    for i in range(num_agents):
        agent_name = 'malmo' + str(i)
        xml += '''<AgentSection mode="Survival">
            <Name>''' + agent_name + '''</Name>
            <AgentStart>
            </AgentStart>
            <AgentHandlers>
                <ObservationFromFullInventory/>
                <ObservationFromFullStats/>
                <ContinuousMovementCommands turnSpeedDegs="180"/>
                <VideoProducer>
                    <Width>''' + str(200) + '''</Width>
                    <Height>''' + str(100) + '''</Height>
                </VideoProducer>
            </AgentHandlers>
          </AgentSection>'''

    xml += '</Mission>'
    return(xml)

# This idiom is required for multiprocessing.
if __name__ == '__main__':

    # Select the desired number of exoelves.
    num_exoselves = 2

    # Build physical exoself addresses locations.
    exoself_addresses = [['127.0.0.1', 10000],
                         ['127.0.0.1', 10001],
                         ['127.0.0.1', 10002],
                         ['127.0.0.1', 10003]]

    exoself_addresses = [['127.0.0.1', 10000+i] for i in range(num_exoselves)]

    # Build the XML for this mission.
    mission_xml = get_mission_xml(num_exoselves)

    # Create a pool of workers to hold the exoselfs.
    worker_pool = Pool(processes=num_exoselves)

    # Instantiate a Queue for communication.
    mind_queue = Queue()

    # Iterate over each physical address to instantiate a worker there.
    for role, exoself_address in enumerate(exoself_addresses):

        # Get the client IP address.
        ip_address = exoself_address[0]

        # Get the client port.
        port = exoself_address[1]

        # Launch a worker which creates and launches an exoself.
        worker_pool.apply_async(me.MinecraftExoself, args=(mission_xml, role,
                                                           exoself_addresses,
                                                           ip_address, port,))

    worker_pool.close()
    worker_pool.join()

    print("At the end...")
