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


def PortHasListener(port):

    # Open a socet to the given port on the local machine.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0


def launchMinecraftClient(port):

    # TO DO: Figure out how to lauch the cmd with a specific port!

    # If on windows.
    if os.name == 'nt':

        # Change Working Dir.
        os.chdir('..\Minecraft')

        # Launch a client
        os.startfile('launchClient.bat')
        #subprocess.Popen(['mintty', '/K', 'launchClient.bat','-port '+str(port)])

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

        subprocess.Popen("x-terminal-emulator -e ./launchClient.sh -prot "+str(port), close_fds=True, shell=True )

        # Change Back.
        os.chdir('..\malmo_net')
    return 0


def build_client_pool(num_clients=1):

    # Iterate for each desired client.
    for client_label in range(num_clients):

        # Launch the client.
        print 'Launching client on port '+str(10000+client_label)
        launchMinecraftClient(10000+client_label)

    # Validate that eack client has loaded before proceeding.
    print 'Giving Minecraft some time to launch... '
    clients_loaded = False
    t = 0

    # Iterate until the clients load or we give up.
    while not(clients_loaded) and (t < 100):

        # Heartbeat, track, and pause.
        t += 1
        print '.'
        time.sleep(1)

        # AND a Boolean vector of indicators for client completion.
        if all([PortHasListener(10000 + c) for c in range(num_clients)]):
            print 'all clients successfully launched.'
            clients_loaded = True

    # Instantiate a new clent pool.
    localClientPool = MalmoPython.ClientPool()

    # Assign each of the newly-created clients to the pool
    for client_label in range(num_clients):

        client_port = 10000+client_label
        localClientPool.add(MalmoPython.ClientInfo("127.0.0.1", client_port))

    # Notify the user of completion.
    print "The following ClientPool was built: "
    print localClientPool

    return localClientPool


def getMissionXML():

    # TO DO: Generate XML programatically for fexibel agent adding.

    missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
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

    #    <ModSettings> 
    #        <MsPerTick> 50 </MsPerTick>
    #        <PrioritiseOffscreenRendering> true </PrioritiseOffscreenRendering>
    #    </ModSettings>
    return(missionXML)


class MinecraftExoself(object):

    # An Exoself is a placeholder for an entity in the world. Thus, Exoselves
    # should be permenant, with different agents assigned to the Exoself,
    # through simulation-time.

    def __init__(self, my_mission, client_pool, my_mission_record,
                 client_role):

        # Build an agent host for this agent.
        agent_host = MalmoPython.AgentHost()

        # Construct a pickling interface function.
        def pickleable_AgentHost_reduce(self):
            return (MalmoPython.AgentHost, ())
        funcType = type(MalmoPython.AgentHost.__reduce__)
        agent_host.__reduce__ = funcType(pickleable_AgentHost_reduce,
                                         agent_host,
                                         MalmoPython.AgentHost)

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

        # Validate the role.
        role = agent_host.getIntArgument("role")
        print "Will run as role", role

        # Initialize the Malmo agent host's observation policy.
        observe_policy = MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY
        agent_host.setObservationsPolicy(observe_policy)

        # Set parameters
        self.agentHost = agent_host
        self.mission = my_mission
        self.clientPool = client_pool
        self.missionRecord = my_mission_record
        self.clientRole = client_role

        # Distinguish the 0-role client, and allow additional time to start up.
        if client_role == 0:

            # Initialize the Malmo mission.
            self.initializeMission()

            # Spin a thread for this player.
            self.setThread(Process(target=self))

            print "Waiting for the launch of client 0."
            time.sleep(15)
            print "The wait is over!"

        else:
            # Initialize the Malmo mission.
            self.initializeMission()

            # Spin a thread for this player.
            self.setThread(Process(target=self))

    def __call__(self):

        # Noify the system that this Exoself is in waitForStart.
        print "Entring waitForStart"

        # Wait for the Mission to begin.
        self.waitForMissionStart()

        print "Exiting waitForStart"

        # Observe the world state.
        world_state = self.agentHost.getWorldState()

        # Loop until the world state indicates that the mission has ended.
        #while world_state.is_mission_running:
        while True:
            
            print ("This message is from Exoself %d." % self.clientRole)
            # Send the heartbeat.
            # sys.stdout.write(".")
            # time.sleep(1)

            # Observe the world state again.
            world_state = self.agentHost.getWorldState()

            # Record state.
            if world_state.number_of_video_frames_since_last_state > 0:
                #print
                #print str(world_state.video_frames[0].pixels)
                #print str(world_state.observations)
                #print
                print ("This message is from Exoself %d." % self.clientRole)

            #self.mind.stimulate()

            # Command the agent.
            actuator_vector = numpy.random.rand(8)
            actuator_vector[0:4] = (actuator_vector[0:4]*2)-1

            self.agentHost.sendCommand("move "+str(actuator_vector[0]))
            self.agentHost.sendCommand("strafe "+str(actuator_vector[1]))
            self.agentHost.sendCommand("pitch "+str(actuator_vector[2]))
            self.agentHost.sendCommand("turn "+str(actuator_vector[3]))

            self.agentHost.sendCommand("jump "+str(actuator_vector[4]))
            self.agentHost.sendCommand("crouch "+str(actuator_vector[5]))
            self.agentHost.sendCommand("attack "+str(actuator_vector[6]))
            self.agentHost.sendCommand("use "+str(actuator_vector[7]))

            # If the world state contains an error, print it.
            for error in world_state.errors:
                print "Error:", error.text

        print("The agent occupying exoself %d has died." % self.clientRoll)

        # Something needs to go here to start a new agent running.
        # The next agent must be provided from the enviroment.

    def waitForMissionStart(self):

        # Observe the world state again.
        world_state = self.agentHost.getWorldState()

        # Repeat until the mission starts.
        while not world_state.is_mission_running:

            # Send a heartbeat.
            sys.stdout.write(".")
            time.sleep(0.1)

            # Observe the world state again.
            world_state = self.agentHost.getWorldState()

            # If the world state contains an error, print it.
            if len(world_state.errors) > 0:
                for err in world_state.errors:
                    print err
                exit(1)

        print "Mission started!"

    def initializeMission(self):
        max_retries = 3
        for retry in range(max_retries):
            try:
                self.agentHost.startMission(self.mission, self.clientPool,
                                            self.missionRecord,
                                            self.clientRole, "test")
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print "Error starting mission:", e
                    exit(1)
                else:
                    time.sleep(2)

    def setThread(self, t):
        self.thread = t

    def setMind(self, mind):
        self.mind = mind

    def start(self):
        self.thread.start()

#class Universe(object):
#
#    #  A universe comprises a set of clients, each of which has both a client
#    # host and an exoself, to which agents are attached.
#    def __init__():
#        return(0)


if __name__ == "__main__":

    # 5Select the desired number of clients.
    num_clients = 2

    # Built the client pool
    client_pool = build_client_pool(num_clients)

    def pickleable_ClientPool_reduce(self):
        return (MalmoPython.ClientPool, ())

    funcType = type(MalmoPython.ClientPool.__reduce__)

    client_pool.__reduce__ = funcType(pickleable_ClientPool_reduce,
                                      client_pool,
                                      MalmoPython.ClientPool)

    # Construct a default mission.
    my_mission = MalmoPython.MissionSpec(getMissionXML(num_clients), True)

    def pickleable_MissionSpec_reduce(self):
        return (MalmoPython.MissionSpec, (getMissionXML(num_clients), True))

    funcType = type(MalmoPython.MissionSpec.__reduce__)

    my_mission.__reduce__ = funcType(pickleable_MissionSpec_reduce, my_mission,
                                     MalmoPython.MissionSpec)

    # Construct the defualt mission record object.
    my_mission_record = MalmoPython.MissionRecordSpec()

    def pickleable_MissionRecordSpec_reduce(self):
        return (MalmoPython.MissionRecordSpec, ())

    funcType = type(MalmoPython.MissionRecordSpec.__reduce__)

    my_mission_record.__reduce__ = funcType(pickleable_MissionRecordSpec_reduce,
                                            my_mission_record,
                                            MalmoPython.MissionRecordSpec)

# Iterate once for each client, constructing an exoself. r must start at 0.
exoselves = [MinecraftExoself(my_mission, client_pool, my_mission_record, r) for r in range(0, num_clients)]

# For each exoself, launch it's thread.
[exoself.start() for exoself in exoselves]

print("I'm done here.")

time.sleep(10)
