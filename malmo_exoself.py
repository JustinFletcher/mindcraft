# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 10:21:14 2016

@author: Justin Fletcher
"""

import os

import sys

import time

import subprocess

import numpy as np

import MalmoPython

import socket


def port_has_listener(ip_address, port):

    # Open a socet to the given port on the local machine.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip_address, port))
    sock.close()
    return result == 0


def launch_minecraft_client(ip_address, port):

    # TODO: Figure out how to lauch the cmd with a specific port!

    # If on windows.
    if os.name == 'nt':

        # Change Working Dir.
        os.chdir('..\Minecraft')

        # Launch a client.
        os.startfile('launchClient.bat')

        # Change Back.
        os.chdir('..\malmo_net')

#    # If on OSX.
#    elif sys.platform == 'darwin':
#
#        # Change Working Dir.
#        os.chdir('..\Minecraft')
#
#        subprocess.Popen(['open', '-a', 'Terminal.app', 'launchClient.sh', '-port '+str(port)])
#
#        # Change Back.
#        os.chdir('..\malmo_net')
#    # If on Linux.
#    elif platform.linux_distribution()[0] == 'Fedora':
#
#        # Change Working Dir.
#        os.chdir('..\Minecraft')
#
#        subprocess.Popen("gnome-terminal -e ./launchClient.sh -port "+str(port), close_fds=True, shell=True)
#
#        # Change Back.
#        os.chdir('..\malmo_net')
    else:

        # Change Working Dir.
        os.chdir('../Minecraft')

        cmd_str = "x-terminal-emulator -e ./launchClient.sh -port " + str(port)

        subprocess.Popen(cmd_str,
                         close_fds=True,
                         shell=True)

        # Change Back.
        os.chdir('../mindcraft')


class MinecraftExoself(object):

    # An Exoself is a placeholder for an entity in the world. Thus, Exoselves
    # should be permenant, with different agents assigned to the Exoself,
    # through simulation-time.

    def __init__(self,
                 mission_xml,
                 exoself_addresses,
                 role_queue,
                 mind_queue):

        role = role_queue.get(True)
        ip_address = exoself_addresses[role][0]
        port = exoself_addresses[role][1]

        # Pause for 1 second per role, to ensure start staggering.
        time.sleep(role)

        # launch a client local to this process.
        launch_minecraft_client(ip_address, port)

        # Confirm that the local client is loaded before proceeding.
        print('Launching client for exoself %d.' % role)
        t = 0

        # Iterate until the clients load or we give up.
        while not(port_has_listener(ip_address, port)):

            # Heartbeat, track, and pause.
            t += 1
            print('.')
            time.sleep(1)

        mission_spec = MalmoPython.MissionSpec(mission_xml, True)

        # Build an agent host for this agent.
        agent_host = MalmoPython.AgentHost()

        # Assign the role description string.
        role_desc = "For multi-agent missions, the role of this agent instance"

        # Assign a role to the Malmo agent host.
        agent_host.addOptionalIntArgument("role,r", role_desc, role)

        # Read input arguements.
        try:
            agent_host.parse(sys.argv)
        except RuntimeError as e:
            print('ERROR:', e)
            print(agent_host.getUsage())
            exit(1)

        # Validate the role.
        role = agent_host.getIntArgument("role")
        print("Will run as role", role)

        # Initialize the Malmo agent host's observation policy.
        obs_policy = MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY
        agent_host.setObservationsPolicy(obs_policy)

        # Build a global client pool.
        global_client_pool = MalmoPython.ClientPool()

        # Iterate over each address, constucting an exoself.
        for client_location in exoself_addresses:

            # Get the client IP address.
            ip_address = client_location[0]

            # Get the client port.
            port = client_location[1]

            # Add this location to the pool.
            global_client_pool.add(MalmoPython.ClientInfo(ip_address, port))

        # Set parameters
        self.agent_host = agent_host
        self.mission = mission_spec
        self.client_pool = global_client_pool
        self.mission_record = MalmoPython.MissionRecordSpec()
        self.role = role
        self.mind_queue = mind_queue

        # Distinguish the 0-role client, and allow additional time to start up.
        if role != 0:

            print("Exoself %d is waiting for client 0 to launch." % self.role)

            # TODO: make this hold depend on client 0's launch.
            time.sleep(30)
            print("The wait is over!")

        # Initialize the Malmo mission.
        self.initialize_mission()

        # Noify the system that this Exoself is in waitForStart.
        print("Entring waitForStart")

        # Wait for the Mission to begin.
        self.await_mission_start()

        print("Exiting waitForStart")

        # Instantiate a new exoself on the local client.
        self.main()

    def main(self):

        # Notify the user of instanitation.
        print("Exoself %d main is called in pid" % self.role)

        while True:

            print("trying to get a mind")

            mind = self.mind_queue.get(True)

            print("trying to set a mind")

            # Block until a mind is put on the queue. Once it is set the mind.
            self.set_mind(mind)

            print("got a mind")

            # Observe the world state.
            world_state = self.agent_host.getWorldState()

            # Loop until the world state indicates that the mission has ended.
            while world_state.is_mission_running:

                print("mission running...")

                # Send the heartbeat.
                time.sleep(0.01)

                # Observe the world state again.
                world_state = self.agent_host.getWorldState()

                # If there is a new state to observe...
                if world_state.number_of_video_frames_since_last_state > 0:

                    # Observe it.
                    stimulus = np.array(world_state.video_frames[0].pixels)

                    # Then, stimulate the mind (agent) hosted in this exoself.
                    actuator_vector = self.mind.stimulate(stimulus)

                    # Command the agent.
                    # actuator_vector = np.random.rand(8)
                    # actuator_vector[0:4] = (actuator_vector[0:4]*2)-1

                    self.agent_host.sendCommand("move " + str(actuator_vector[0]))
                    self.agent_host.sendCommand("strafe " + str(actuator_vector[1]))
                    self.agent_host.sendCommand("pitch " + str(actuator_vector[2]))
                    self.agent_host.sendCommand("turn " + str(actuator_vector[3]))

                    self.agent_host.sendCommand("jump " + str(actuator_vector[4]))
                    self.agent_host.sendCommand("crouch " + str(actuator_vector[5]))
                    self.agent_host.sendCommand("attack " + str(actuator_vector[6]))
                    self.agent_host.sendCommand("use " + str(actuator_vector[7]))

                # If the world state contains an error, print it.
                for error in world_state.errors:
                    print("Error:", error.text)

            print("The agent occupying exoself %d has died." % self.client_role)

    def await_mission_start(self):

        # Observe the world state again.
        world_state = self.agent_host.getWorldState()

        # Repeat until the mission starts.
        while not world_state.is_mission_running:

            # Send a heartbeat.
            sys.stdout.write(".")
            time.sleep(0.1)

            # Observe the world state again.
            world_state = self.agent_host.getWorldState()

            # If the world state contains an error, print it.
            if len(world_state.errors) > 0:
                for err in world_state.errors:
                    print(err)
                exit(1)

        print("Mission started!")

    def initialize_mission(self):

        max_retries = 3
        for retry in range(max_retries):
            try:
                self.agent_host.startMission(self.mission, self.client_pool,
                                             self.mission_record,
                                             self.role, "")
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:", e)
                    exit(1)
                else:
                    time.sleep(2)

    def set_thread(self, t):
        self.thread = t

    def set_mind(self, mind):
        self.mind = mind.build()
