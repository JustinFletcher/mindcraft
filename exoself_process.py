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

# Print the current working directory.
print os.getcwd()

# flush print output immediately.
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


def port_has_listener(port):

    # Open a socet to the given port on the local machine.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0


def launch_minecraft_client(ip_address, port):

    # TO DO: Figure out how to lauch the cmd with a specific port!

    # If on windows.
    if os.name == 'nt':

        # Change Working Dir.
        os.chdir('..\Minecraft')

        # Launch a client.
        os.startfile('launchClient.bat')

        # Change Back.
        os.chdir('..\malmo_net')

    # If on OSX.
    elif sys.platform == 'darwin':

        # Change Working Dir.
        os.chdir('..\Minecraft')

        subprocess.Popen(['open', '-a', 'Terminal.app', 'launchClient.sh', '-port '+str(port)])

        # Change Back.
        os.chdir('..\malmo_net')
    # If on Linux.
    elif platform.linux_distribution()[0] == 'Fedora':

        # Change Working Dir.
        os.chdir('..\Minecraft')

        subprocess.Popen( "gnome-terminal -e ./launchClient.sh -port "+str(port), close_fds=True, shell=True )

        # Change Back.
        os.chdir('..\malmo_net')
    else:

        # Change Working Dir.
        os.chdir('..\Minecraft')

        subprocess.Popen( "x-terminal-emulator -e ./launchClient.sh -prot "+str(port), close_fds=True, shell=True )

        # Change Back.
        os.chdir('..\malmo_net')

    return 0


def get_mission_xml(num_agents=1):

    # TO DO: Generate XML programatically for fexibel agent adding.

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
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>malmo0</Name>
            <AgentStart>
            </AgentStart>
            <AgentHandlers>
                <ObservationFromFullInventory/>
                <ObservationFromFullStats/>
                <ContinuousMovementCommands turnSpeedDegs="180"/>
                <VideoProducer>
                    <Width>''' + str(256) + '''</Width>
                    <Height>''' + str(256) + '''</Height>
                </VideoProducer>
            </AgentHandlers>
        </AgentSection>

        <AgentSection mode="Survival">
            <Name>malmo1</Name>
            <AgentStart>
            </AgentStart>
            <AgentHandlers>
                <ObservationFromFullInventory/>
                <ObservationFromFullStats/>
                <ContinuousMovementCommands turnSpeedDegs="180"/>
                <VideoProducer>
                    <Width>''' + str(256) + '''</Width>
                    <Height>''' + str(256) + '''</Height>
                </VideoProducer>
            </AgentHandlers>
        </AgentSection>

        <AgentSection mode="Survival">
            <Name>malmo2</Name>
            <AgentStart>
            </AgentStart>
            <AgentHandlers>
                <ObservationFromFullInventory/>
                <ObservationFromFullStats/>
                <ContinuousMovementCommands turnSpeedDegs="180"/>
                <VideoProducer>
                    <Width>''' + str(256) + '''</Width>
                    <Height>''' + str(256) + '''</Height>
                </VideoProducer>
            </AgentHandlers>
        </AgentSection>

        <AgentSection mode="Survival">
            <Name>malmo3</Name>
            <AgentStart>
            </AgentStart>
            <AgentHandlers>
                <ObservationFromFullInventory/>
                <ObservationFromFullStats/>
                <ContinuousMovementCommands turnSpeedDegs="180"/>
                <VideoProducer>
                    <Width>''' + str(256) + '''</Width>
                    <Height>''' + str(256) + '''</Height>
                </VideoProducer>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''

#    for i in range(num_agents):
#        agent_name = 'malmo' + str(i)
#        xml += '''<AgentSection mode="Survival">
#            <Name>''' + agent_name + '''</Name>
#            <AgentStart>
#            </AgentStart>
#            <AgentHandlers>
#                <ObservationFromFullInventory/>
#                <ObservationFromFullStats/>
#                <ContinuousMovementCommands turnSpeedDegs="180"/>
#                <VideoProducer>
#                    <Width>''' + str(256) + '''</Width>
#                    <Height>''' + str(256) + '''</Height>
#                </VideoProducer>
#            </AgentHandlers>
#          </AgentSection>'''
#
#    xml += '</Mission>'
    #    <ModSettings> 
    #        <MsPerTick> 50 </MsPerTick>
    #        <PrioritiseOffscreenRendering> true </PrioritiseOffscreenRendering>
    #    </ModSettings>
    return(xml)


class MinecraftExoself(object):

    # An Exoself is a placeholder for an entity in the world. Thus, Exoselves
    # should be permenant, with different agents assigned to the Exoself,
    # through simulation-time.

    def __init__(self, my_mission, client_location_list, my_mission_record,
                 client_role):

        # Notify the user of instanitation.
        print("Exoself %d __init__ is called" % client_role)

        # Build an agent host for this agent.
        agent_host = MalmoPython.AgentHost()

        # Assign the role description string.
        role_desc = "For multi-agent missions, the role of this agent instance"

        # Assign a role to the Malmo agent host.
        agent_host.addOptionalIntArgument("role,r", role_desc, client_role)

        # Read input arguements.
        try:
            agent_host.parse(sys.argv)
        except RuntimeError as e:
            print 'ERROR:', e
            print agent_host.getUsage()
            exit(1)
        if agent_host.receivedArgument("help"):
            print agent_host.getUsage()
            exit(0)

        # Validate the role.
        role = agent_host.getIntArgument("role")
        print "Will run as role", role

        # Initialize the Malmo agent host's observation policy.
        obs_policy = MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY
        agent_host.setObservationsPolicy(obs_policy)

        # Build a global client pool.
        global_client_pool = MalmoPython.ClientPool()

        # Iterate over each address, constucting an exoself.
        for client_location in client_location_list:

            # Get the client IP address.
            ip_address = client_location[0]

            # Get the client port.
            port = client_location[1]

            # Add this location to the pool.
            global_client_pool.add(MalmoPython.ClientInfo(ip_address, port))

        # Set parameters
        self.agent_host = agent_host
        self.mission = my_mission
        self.client_pool = global_client_pool
        self.mission_record = my_mission_record
        self.client_role = client_role

        # Distinguish the 0-role client, and allow additional time to start up.
        if client_role != 0:

            print "Waiting for the launch of client 0."
            time.sleep(15)
            print "The wait is over!"

        # Initialize the Malmo mission.
        self.initialize_mission()

        # Spin a thread for this player.
        self.launch_exoself()

    def launch_exoself(self):

        # Noify the system that this Exoself is in waitForStart.
        print "Entring waitForStart"

        # Wait for the Mission to begin.
        self.await_mission_start()

        print "Exiting waitForStart"

        # Observe the world state.
        world_state = self.agent_host.getWorldState()

        # Loop until the world state indicates that the mission has ended.
        while world_state.is_mission_running:

            # Send the heartbeat.
            time.sleep(1)

            # Observe the world state again.
            world_state = self.agent_host.getWorldState()

            # Record state.
            if world_state.number_of_video_frames_since_last_state > 0:
                #print 
                #print str(world_state.video_frames[0].pixels)
                #print str(world_state.observations)
                #print
                print ("This message is from Exoself %d." % self.client_role)

            # self.mind.stimulate()

            # Command the agent.
            actuator_vector = numpy.random.rand(8)
            actuator_vector[0:4] = (actuator_vector[0:4]*2)-1

            self.agent_host.sendCommand("move "+str(actuator_vector[0]))
            self.agent_host.sendCommand("strafe "+str(actuator_vector[1]))
            self.agent_host.sendCommand("pitch "+str(actuator_vector[2]))
            self.agent_host.sendCommand("turn "+str(actuator_vector[3]))

            self.agent_host.sendCommand("jump "+str(actuator_vector[4]))
            self.agent_host.sendCommand("crouch "+str(actuator_vector[5]))
            self.agent_host.sendCommand("attack "+str(actuator_vector[6]))
            self.agent_host.sendCommand("use "+str(actuator_vector[7]))

            # If the world state contains an error, print it.
            for error in world_state.errors:
                print "Error:", error.text

        print("The agent occupying exoself %d has died." % self.client_role)

        # Something needs to go here to start a new agent running.
        # The next agent must be provided from the enviroment.

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
                    print err
                exit(1)

        print "Mission started!"

    def initialize_mission(self):

        print(self.client_pool)
        max_retries = 3
        for retry in range(max_retries):
            try:
                self.agent_host.startMission(self.mission, self.client_pool,
                                             self.mission_record,
                                             self.client_role, "")
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print "Error starting mission:", e
                    exit(1)
                else:
                    time.sleep(2)

    def set_thread(self, t):
        self.thread = t

    def set_mind(self, mind):
        self.mind = mind

# Select the desired number of exoelves.
num_exoselves = 4

serverAddress = "127.0.0.1"

serverPort = 10000


def create_exoself(role, exoself_addresses, ip_address, port):

        # launch a client local to this process.
        launch_minecraft_client(ip_address, port)

        # Confirm that the local client is loaded before proceeding.
        print 'Giving Minecraft some time to launch... '
        t = 0

        # Iterate until the clients load or we give up.
        while not(port_has_listener(port)) and (t < 100):

            # Heartbeat, track, and pause.
            t += 1
            print '.',
            time.sleep(1)

        mission_spec = MalmoPython.MissionSpec(get_mission_xml(), True)

        # Instantiate a new exoself on the local client.
        exoself = MinecraftExoself(mission_spec, exoself_addresses,
                                   MalmoPython.MissionRecordSpec(), role)

        return(exoself)

# This idiom is required for multiprocessing.
if __name__ == '__main__':

    # Build physical exoself addresses locations.
    exoself_addresses = [["127.0.0.1", 10000], ["127.0.0.1", 10001], ["127.0.0.1", 10002], ["127.0.0.1", 10003]]

    # Instantiate a list to hold the processes.
    exoself_processes = []

    for role, exoself_address in enumerate(exoself_addresses):

        # Get the client IP address.
        ip_address = exoself_address[0]

        # Get the client port.
        port = exoself_address[1]

        # Create a process.
        p = Process(target=create_exoself,
                    args=(role, exoself_addresses, ip_address, port,))

        # Add the process to the list.
        exoself_processes.append(p)

    # Create a list of processes, each of which is running an exoself process.
    [exoself_process.start() for exoself_process in exoself_processes]
