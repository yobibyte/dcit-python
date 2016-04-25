from threading import Thread
import os
from Util import get_node_by_addr


class Cli(Thread):

    def __init__(self, api):
        Thread.__init__(self)
        print("Client created")
        self.api = api

    def process_command(self, cmd):
        args = cmd.split()
        if len(args) == 0:
            args = [""]

        if args[0] == 'join':
            self.api.join(args[1])
            self.api.setStatus(True)
            print("Joined. You're online, lucky!")
        elif args[0] == "logoff":
            status = self.api.getStatus()
            if status:
                self.api.leave()
                out = "You're logged off. Bye."
            else:
                out = "Hey! You're already offline. What do you want from me?"
                print(out)
        elif args[0] == "exit":
            out = "Self-destruction program started. We will never see each other again =( "
            print(out)
            os._exit(1)
        elif args[0] == "elections":
            print("Elections started")
            self.api.runBully()
        elif args[0] == "show":
            print(self.api.getNetworkMembers())
        elif args[0] == "master":
            print("Master node is " + self.api.getMasterAddress())
        elif args[0] == "fun":
            print("Having fun right now")
            self.api.adventureTime(False)
        elif args[0] == "agrawala":
            print("Having agrawalafun right now")
            self.api.adventureTime(True)
        elif args[0] == "ms":
            self.api.checkMasterAvaliability()
            print("Master string is " + self.api.getMasterString())
        elif args[0] == "cleanms":
            get_node_by_addr(self.api.getMasterAddress()).setMasterString("")
            print("Cleaned master string")
        else:
            print("Unknown command. Check the manual")

    def run(self):
        print("Client started")
        while True:
            print("Enter your command")
            cmd = input()
            try:
                self.process_command(cmd)
            except:
                print("Something went wrong, please contact Microsoft support")
