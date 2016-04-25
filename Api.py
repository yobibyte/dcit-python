from Util import *

class Api:

    def _dispatch(self, name, args):
        if name == 'Api.getMasterAddress':
            return self.getMasterAddress()
        elif name == 'Api.appendNode':
            return self.appendNode(args[0])
        elif name == 'Api.setMasterAddress':
            return self.setMasterAddress(args[0])
        elif name == 'Api.getNetworkMembers':
            return self.getNetworkMembers()
        elif name == 'Api.leave':
            return self.leave()
        elif name == 'Api.setStatus':
            return self.setStatus(args[0])
        elif name == 'Api.getStatus':
            return self.getStatus()
        elif name == 'Api.deleteNode':
            return self.deleteNode(args[0])
        elif name == 'Api.runBully':
            return self.runBully()
        elif name == 'Api.setVictoryBroadcasted':
            return self.setVictoryBroadcasted(args[0])
        elif name == 'Api.setMaster':
            return self.setMaster(args[0])
        elif name == 'Api.getWordListToCheck':
            return self.getWordListToCheck()
        elif name == 'Api.appendMasterStringRequest':
            return self.appendMasterStringRequest(args[0])
        elif name == 'Api.appendMasterStringRelease':
            return self.appendMasterStringRelease(args[0])
        elif name == 'Api.agrawalaAppendHandle':
            return self.agrawalaAppendHandle(args[0])
        elif name == 'Api.getMasterString':
            return self.getMasterString()
        elif name == 'Api.haveFun':
            return self.haveFun(args[0])
        elif name == 'Api.electionBroadcast':
            return self.electionBroadcast(args[0])
        elif name == 'Api.setMasterString':
            return self.setMasterString(args[0])
        elif name == 'Api.checkAppend':
            return self.checkAppend()
        elif name == 'Api.checkMasterAvaliability':
            return self.checkMasterAvaliability()



    def __init__(self, serv):
        self.serv = serv
        print("Api created")

    def leave(self):
        self.serv.leave()
        return True

    def join(self, addr):
        self.serv.join_net(addr)
        return True

    def setStatus(self, st):
        self.serv.set_status(st)
        return True

    def getStatus(self):
        return self.serv.get_status()

    def getNetworkMembers(self):
        return self.serv.get_net_members()

    def appendNode(self, addr):
        self.serv.append_node(addr)
        return True

    def deleteNode(self, address):
        self.serv.delete_node(address)
        return True

    def getMasterString(self):
        return self.serv.get_master_string()

    def getMasterAddress(self):
        return self.serv.get_master_address()

    def haveFun(self, isAgrawala):
        self.serv.have_fun(isAgrawala)
        return True

    def adventureTime(self, isAgrawala):
        self.serv.adventure_time(isAgrawala)
        return True

    def runBully(self):
        self.serv.run_bully()
        return True

    def electionBroadcast(self, source_addr):
        self.serv.election_broadcast(source_addr)
        return True

    def setVictoryBroadcasted(self, status):
        self.serv.set_victory_broadcasted(status)
        return True

    def agrawalaAppendHandle(self, timestamp):
        self.serv.agrawala_append_handler(timestamp)
        return True

    def appendMasterStringRequest(self, addr):
        self.serv.append_master_string_request(addr)
        return True

    def setMasterString(self, s):
        self.serv.set_master_string(s)
        return True

    def appendMasterString(self, s):
        self.serv.append_master_string(s)
        return True

    def setMasterAddress(self, addr):
        self.serv.set_master_addr(addr)
        return True

    def setMaster(self, newIp):
        self.serv.set_master(newIp)

    def getWordListToCheck(self):
        return self.serv.get_word_list_to_check()

    def appendMasterStringRelease(self, sourceAddr):
        self.serv.apppend_master_string_release(sourceAddr)
        return True

    def checkAppend(self):
        self.serv.checkAppend()
        return True

    def checkMasterAvaliability(self):
        self.serv.check_master_avaliability()
        return True
