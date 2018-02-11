# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 15:58:08 2016

@author: Justin Fletcher
# @title: 
"""


import MalmoPython
import os
import sys
import time
import numpy as np
import platform
import socket
import subprocess

from multiprocessing import Process
from multiprocessing import Pool
from multiprocessing import Queue

from sys import executable
# from subprocess import Popen, CREATE_NEW_CONSOLE


# sys.path.insert(0, 'C:/Malmo/malmo_net/')
# sys.path.insert(0, 'C:/neurocomputation')
import malmo_exoself as me

# sys.path.insert(0, '/home/justin/research/neurocomputation')
sys.path.insert(0, 'C:/Users/Justi/Research/neurocomputation')
import neurocomputation as nc

# Print the current working directory.
print(os.getcwd())

# flush print output immediately.
# sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


def get_mission_xml(num_agents=1, window_height=256, window_width=256):

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
                    <Width>''' + str(window_width) + '''</Width>
                    <Height>''' + str(window_height) + '''</Height>
                </VideoProducer>
            </AgentHandlers>
          </AgentSection>'''

    xml += '</Mission>'
    return(xml)


# This idiom is required for multiprocessing.
if __name__ == '__main__':

    # Select the desired number of exoselves.
    num_exoselves = 2

    # Build physical exoself addresses locations.
    exoself_addresses = [['127.0.0.1', 10000],
                         ['127.0.0.1', 10001],
                         ['127.0.0.1', 10002],
                         ['127.0.0.1', 10003]]

    exoself_addresses = [['127.0.0.1', 10000 + i]
                         for i in range(num_exoselves)]

    # Build the XML for this mission.
    window_height = 100
    window_width = 300
    mission_xml = get_mission_xml(num_exoselves,
                                  window_height=window_height,
                                  window_width=window_width)

    # Instantiate a Queue for communication.
    mind_queue = Queue()
    role_queue = Queue()

    [role_queue.put(i) for i in range(num_exoselves)]

    # Create a pool of workers to hold the exoselves.
    worker_pool = Pool(processes=num_exoselves,
                       initializer=me.MinecraftExoself,
                       initargs=(mission_xml,
                                 exoself_addresses,
                                 role_queue,
                                 mind_queue))

    for i in range(num_exoselves):

        # Set network parameters.
        layer_size_list = [3 * (window_height * window_width), 10, 8]
        activation_function = np.tanh
        scale = 0.001

        # Builds a random network generator from the specifications.
        mind_builder = nc.FeedForwardNeuralNetworkBuilder(layer_size_list,
                                                          act_function=np.tanh,
                                                          scale=scale)

        # Add the instantiated network to the queue of agents.
        mind_queue.put(mind_builder)
        print("put a net on the queue")

    worker_pool.close()
    worker_pool.join()

print("And I'm done.")
