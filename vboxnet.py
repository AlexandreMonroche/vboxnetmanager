#! /usr/bin/env python3
# coding: utf-8

"""
[EN]
This script allows to interact with VirtualBox to list, create or delete private host networks "vboxnet"
-------------------------------------------------------------------------------------------------------------
Ce script permet d'intéragir avec VirtualBox pour lister, créer ou supprimer des réseaux privé hôte "vboxnet"
[FR]
"""

# Libraries imports
import argparse, os, subprocess

# Arguments definition
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", nargs='?', const=1, default=0, help="""Create the network""")
    parser.add_argument("-r", "--remove", action='store_true', help="""Remove the network""")
    parser.add_argument("-l", "--list", action='store_true', help="""List all networks""")
    return parser.parse_args()

# Retrieve the list of existing networks
def catchNetworkList():
    # System command whose output is written in the "networklist" file
    os.system("vboxmanage list hostonlyifs > networklist")

    # We get the list in the "networklist" file
    f = open('networklist', 'r')
    networkList = f.readlines()
    f.close()

    # Deleting the file
    os.system('rm networklist')

    return networkList


def main():
    # Set the network limit
    networkLimit = 20

    # Catch of the arguments
    args = parse_arguments()

    # Recover the list of networks
    networkList = catchNetworkList()

    # Length of this list
    longueurNetworkList = len(networkList)

    # Each network occupies 13 lines in the output of the command
    # Dividing the total length by 13, we obtain the number of networks
    nbNetwork = longueurNetworkList // 13

    if args.create:
        # Manage creation with the limit of networks
        if nbNetwork + int(args.create) > networkLimit:
            create = networkLimit - nbNetwork
            print('This script limits the number of networks to ' + str(networkLimit))
            if create != 0: print('Only ' + str(create) + ' networks will be created')
            else: print('No network will be created')
        else: create = int(args.create)

        # We create the required number of networks
        for i in range(create):
            os.system("vboxmanage hostonlyif create")

        # Display of the number of created networks
        if create != 0: print(str(create) + ' networks were created')

    if args.remove:
        # We create a decreasing loop from the number of networks-1 to 0
        # Exemple with 3 networks: vboxnet2 - vboxnet1 - vboxnet0
        for i in range(nbNetwork - 1, -1, -1):
            # vboxnet(i) (exemple: vboxnet3)
            print('vboxnet' + str(i))
            os.system("vboxmanage hostonlyif remove vboxnet" + str(i))

        # Display of the number of deleted networks
        print(str(nbNetwork) + ' networks were removed.')

    if args.list:
        # Display of the number of networks and the list.
        if longueurNetworkList != 0:
            print('\n' + str(nbNetwork) + ' networks :\n')
            os.system("vboxmanage list hostonlyifs")

        # If the list is empty, no networks
        else: print("\nNo network")

if __name__ == "__main__":
    main()
