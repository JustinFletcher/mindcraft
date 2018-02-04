# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 10:55:49 2016

@author: Justin Fletcher
"""

import socket
import os
import time
import MalmoPython
import malmo_exoself as me

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


def create_exoself(mission_xml, role, exoself_addresses, ip_address, port):

        # Pause for 1 second per role, to ensure start staggering.
        time.sleep(role)

        # launch a client local to this process.
        launch_minecraft_client(ip_address, port)

        # Confirm that the local client is loaded before proceeding.
        print('Launching client for exoself %d.' % role)
        t = 0

        # Iterate until the clients load or we give up.
        while not(port_has_listener(port)) and (t < 100):

            # Heartbeat, track, and pause.
            t += 1
            print '.',
            time.sleep(1)

        mission_spec = MalmoPython.MissionSpec(mission_xml, True)

        # Instantiate a new exoself on the local client.
        exoself = me.MinecraftExoself(mission_spec, exoself_addresses,
                                      MalmoPython.MissionRecordSpec(), role)

        return(exoself)
