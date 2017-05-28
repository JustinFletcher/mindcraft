# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 20:31:07 2016

@author: Justin Fletcher
"""

import MalmoPython
import os
import random
import sys
import time
import json
import random
import errno
import numpy

# Define a MinecraftAgent class

class MinecraftBody(object):
    
    def __init__(self, body_host):
        self.body_host = body_host
        self.host = body_host.agent_host
        body_host.start()
    
    def wait_for_mission_start(self):
        
        # Observe the world state again.
        world_state = self.host.getWorldState()
        
        while not world_state.is_mission_running:
            # Send the heartbeat.
            sys.stdout.write(".")
            time.sleep(0.1)
            
            # Observe the world state again.
            world_state = self.host.getWorldState()
            
            # If the world state contains an error, print it.
            if len(world_state.errors) > 0:
                for err in world_state.errors:
                    print err
                exit(1)
                
        print "Mission started!"    
    
    def __call__(self):
        
         # Wait for the Mission to begin.
        self.wait_for_mission_start(self.agent_host)
    
        # Observe the world state.    
        world_state = self.agent_host.getWorldState()
        
        # Loop until the world state indicates that the mission has ended.
        while world_state.is_mission_running:
            
            # Send the heartbeat.
            sys.stdout.write(".")
            time.sleep(1)
            
            # Observe the world state again.
            world_state = self.host.getWorldState()
            
                
            if world_state.number_of_video_frames_since_last_state>0:
                print
                print str(world_state.video_frames[0].pixels)
                print str(world_state.observations)
                print
                
            # Command the agent.    
            actuator_vector = numpy.random.rand(8)
            actuator_vector[0:4] = (actuator_vector[0:4]*2)-1
            self.host.sendCommand("move "+str(actuator_vector[0]))
            self.host.sendCommand("strafe "+str(actuator_vector[1]))
            self.host.sendCommand("pitch "+str(actuator_vector[2]))
            self.host.sendCommand("turn "+str(actuator_vector[3]))
            
            self.host.sendCommand("jump "+str(actuator_vector[4]))
            self.host.sendCommand("crouch "+str(actuator_vector[5]))
            self.host.sendCommand("attack "+str(actuator_vector[6]))
            self.host.sendCommand("use "+str(actuator_vector[7]))
        
        
            # If the world state contains an error, print it.
            for error in world_state.errors:
                print "Error:",error.text
        
        print
        print "*dies*"
        

def wait_for_mission_start(agent_host):
    # Observe the world state again.
    world_state = agent_host.getWorldState()
    while not world_state.is_mission_running:
        # Send the heartbeat.
        sys.stdout.write(".")
        time.sleep(0.1)
        
        # Observe the world state again.
        world_state = agent_host.getWorldState()
        
        # If the world state contains an error, print it.
        if len(world_state.errors) > 0:
            for err in world_state.errors:
                print err
            exit(1)
    print "Mission started!"
    
    
def run_agent(role, my_mission, local_client_pool, my_mission_record, unique_experiment_id, client_pool):
    print 'run agent invoked for agent '+str(role)
    
    # Build an agent host for this agent.
    agent_host = MalmoPython.AgentHost()

    # Assign a role to the agent.
    agent_host.addOptionalIntArgument( "role,r", "For multi-agent missions, the role of this agent instance", role)
  
    # Read input arguements
    try:
        agent_host.parse( sys.argv )
    except RuntimeError as e:
        print 'ERROR:',e
        print agent_host.getUsage()
        exit(1)
    if agent_host.receivedArgument("help"):
        print agent_host.getUsage()
        exit(0)
    
    # Validate the role.
    role = agent_host.getIntArgument("role")
    print "Will run as role",role
    
    agent_host.setObservationsPolicy(MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY)
        
    max_retries = 3
    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, client_pool, my_mission_record, role, unique_experiment_id )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print "Error starting mission:",e
                exit(1)
            else:
                time.sleep(2)
    
    # Wait for the Mission to begin.
    wait_for_mission_start(agent_host)

    # Observe the world state.    
    world_state = agent_host.getWorldState()
    
    # Loop until the world state indicates that the mission has ended.
    while world_state.is_mission_running:
        
        # Send the heartbeat.
        sys.stdout.write(".")
        time.sleep(1)
        
        # Observe the world state again.
        world_state = agent_host.getWorldState()
        
            
        if world_state.number_of_video_frames_since_last_state>0:
            print
            print str(world_state.video_frames[0].pixels)
            print str(world_state.observations)
            print
            
        # Command the agent.    
        actuator_vector = numpy.random.rand(8)
        actuator_vector[0:4] = (actuator_vector[0:4]*2)-1
        agent_host.sendCommand("move "+str(actuator_vector[0]))
        agent_host.sendCommand("strafe "+str(actuator_vector[1]))
        agent_host.sendCommand("pitch "+str(actuator_vector[2]))
        agent_host.sendCommand("turn "+str(actuator_vector[3]))
        
        agent_host.sendCommand("jump "+str(actuator_vector[4]))
        agent_host.sendCommand("crouch "+str(actuator_vector[5]))
        agent_host.sendCommand("attack "+str(actuator_vector[6]))
        agent_host.sendCommand("use "+str(actuator_vector[7]))
    
    
        # If the world state contains an error, print it.
        for error in world_state.errors:
            print "Error:",error.text
    
    print
    print "Mission ended"
    
    
    
if __name__ == "__main__":
    print "I'm here....."
    print sys.argv
    run_agent(sys.argv)