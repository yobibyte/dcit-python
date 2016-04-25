from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer
from Api import Api
from Clock import Clock
import time
import random
from Util import *
import threading
from collections import deque
from socketserver import ThreadingMixIn

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class Serv(Thread):

    def __init__(self, port):
        Thread.__init__(self)
        ip = socket.gethostbyname(socket.gethostname())
        self.server = SimpleThreadedXMLRPCServer((ip, port), allow_none=True)
        self.server.register_introspection_functions()
        self.server.register_multicall_functions()
        self.server.register_instance(Api(self), allow_dotted_names=True)
        self.ctr = 0
        self.addr = ip + ":" + str(port)
        self.net_members = [self.addr]
        self.string_queue = deque() 
        self.status = False
        self.master_string = ""
        self.master_address = ""
        self.is_interested_in_master_string = False
        self.is_victory_broadcasted = False
        self.clock = Clock(self.addr)
        self.wordListToCheck = []
        print("Serv created")


    def run(self):
        self.server.serve_forever()
        print("Serv started")

    def incr(self):
        self.ctr += 1
        print(self.ctr)

    def get_clock(self):
        return self.clock

    def leave(self):
        self.net_members.remove(self.addr)
        self.set_status(False)
        for node in self.net_members:
            get_node_by_addr(node).deleteNode(self.addr)
        if(self.master_address == self.addr and len(self.net_members) > 1):
            get_node_by_addr(self.net_members[0]).runBully()
        for node in self.net_members:
            get_node_by_addr(node).setVictoryBroadcasted(False)
        self.net_members = [self.addr]
        self.master_address = ""
        self.masterString = ""
        self.is_victory_broadcasted = False;




    def join_net(self, addr):
        if addr.startswith("127.0.0.1") or addr.startswith("localhost"):
            asp = addr.split(":")
            ip = socket.gethostbyname(socket.gethostname())
            addr = ip + ":" + asp[1]

        destApi = get_node_by_addr(addr)

        for node in destApi.getNetworkMembers():
            if node not in self.net_members:
                self.net_members.append(node)

        for node in self.net_members:
            if self.addr != node:
                get_node_by_addr(node).appendNode(self.addr)

        if destApi.getMasterAddress() == "":
            self.run_bully()
            for node in self.net_members:
                get_node_by_addr(node).setVictoryBroadcasted(False)
        else:
            self.master_address = destApi.getMasterAddress()


    def set_status(self, st):
        self.status = st

    def get_status(self):
        return self.status

    def get_net_members(self):
        return self.net_members

    def set_net_members(self, members):
        self.net_members = members

    def append_node(self, addr):
        self.status = True
        if addr not in self.net_members:
            print("Adding node " + addr)
            self.net_members.append(addr)

    def delete_node(self, address):
        if address in self.net_members:
            self.net_members.remove(address)
        if len(self.net_members) == 1:
            self.status = False

    def get_master_string(self):
        if self.master_address == self.addr:
            return self.master_string
        else:
            return get_node_by_addr(self.master_address).getMasterString()

    def get_master_address(self):
        return self.master_address

    def have_fun(self, isAgrawala):
        self.wordListToCheck = []
        print("Having fun")
        master = get_node_by_addr(self.master_address)
        stTime = time.time()
        while (time.time() - stTime) < 20:
            time.sleep(random.randint(1,20))
            w = get_random_word()
            self.wordListToCheck.append(w)

            if not isAgrawala:
                print("Sent request for access critical section")
                master.appendMasterStringRequest(self.addr)
                print("Entering critical section")
                ms = master.getMasterString()
                print("Got master string " + ms)
                master.setMasterString(ms+w)
                print("Appending word " + w)
                master.appendMasterStringRelease(self.addr)
                print("Left critical section")
            else:
                self.agrawala_append_string_request(w)

    def adventure_time(self, isAgrawala):
        print("Adventure time!")
        self.check_master_avaliability()

        threads = []
        for node in self.net_members:
            a = get_node_by_addr(node)
            t = threading.Thread(target=a.haveFun, args=(isAgrawala,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        for node in self.net_members:
            a = get_node_by_addr(node)
            a.checkAppend()


    def checkAppend(self):
            ms = self.get_master_string()
            print("Node: " + self.addr + ", master string: " + ms);
            failedWords = []
            for word in self.wordListToCheck:
                if word not in ms:
                   failedWords.append(word)

            if len(failedWords) == 0:
                print("All the appended words are in the master string: " + ','.join(self.wordListToCheck))
            else:
                print("The following words were not appended into master string " + ','.join(failedWords))

    def run_bully(self):
        electionSleepTime = 1
        isThereAnybodyHere = False

        threads = []
        for node in self.net_members:
            if node > self.addr:
                try:
                    a = get_node_by_addr(node)
                    t1 = threading.Thread(target=a.runBully)
                    t1.start()
                    threads.append(t1)
                    isThereAnybodyHere = True
                except ValueError as e:
                    print(e)

        for t in threads:
            t.join()

        if isThereAnybodyHere:
            time.sleep(electionSleepTime)
            if not self.is_victory_broadcasted:
                self.run_bully()
        else:
            for node in self.net_members:
                get_node_by_addr(node).setVictoryBroadcasted(True)
            self.set_master(self.addr)

    def election_broadcast(self, source_addr):
        print("Broadcasting elections")
        threading.Thread(target=self.run_bully).start()
        return True

    def set_victory_broadcasted(self, status):
        print("broadcasting victory")
        self.is_victory_broadcasted = status

    def agrawala_append_string_request(self, word):
        self.clock.tick()
        threads = []
        for node in self.net_members:
            if not self.addr == node:
                a = get_node_by_addr(node)
                self.clock.tick()
                cl = self.clock.get_val()
                t = threading.Thread(target=a.agrawalaAppendHandle, args=(cl,))
                threads.append(t)
                t.start()

        for t in threads:
            t.join()

        print("Node is in critical section")
        self.clock.tick()
        master = get_node_by_addr(self.master_address)
        print("Want to append word " + word)
        self.clock.tick()
        ms = master.getMasterString()
        print("Got master string:" + ms)
        self.clock.tick()
        master.setMasterString(ms+word)
        self.clock.tick()
        self.is_interested_in_master_string = False
        print("Left critical section")
        self.clock.tick()

    def agrawala_append_handler(self, timestamp):
        self.clock.tick()
        if self.clock.get_val().get("val") < timestamp.get("val"):
            self.clock.set_clock(timestamp.get("val") + 1)
        else:
            self.clock.tick()
        while self.is_interested_in_master_string and self.clock.compareTo(timestamp) < 0:
            time.sleep(1)
        self.clock.tick()

    def append_master_string_request(self, source_addr):
        self.string_queue.appendleft(source_addr)
        while self.string_queue[-1] != source_addr:
            time.sleep(1)

    def set_master_string(self, s):
        self.master_string = s

    def append_master_string(self, s):
        self.master_string += s

    def set_master_addr(self, addr):
        self.master_address = addr

    def set_master(self, newIp):
        print("New master elected with addr " + newIp)
        #get old params
        oldString = ""
        try:
            oldMaster = get_node_by_addr(self.master_address)
            oldString = oldMaster.getMasterString()
            oldMaster.setMasterString("")
        except:
            pass

        #find new master
        newMaster = get_node_by_addr(newIp)
        newMaster.setMasterString(oldString)

        #set master ip for others
        for node in self.net_members:
            get_node_by_addr(node).setMasterAddress(newIp)
        #TODO may be it is worth setting isVictoryBroadcasted to false here and in Java

    def get_addr(self):
        return self.addr

    def check_master_avaliability(self):
        #checking if master is alive
        try:
            get_node_by_addr(self.master_address).getStatus()
        except:
            self.net_members.remove(self.master_address)
            for node in self.net_members:
                get_node_by_addr(node).deleteNode(self.master_address)
            self.run_bully()

    def get_word_list_to_check(self):
        return self.wordListToCheck

    def apppend_master_string_release(self, sourceAddr):
        if self.string_queue[-1] == sourceAddr: #todo check popping queue
            self.string_queue.pop()
