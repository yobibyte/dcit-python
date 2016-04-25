import argparse
from Serv import Serv
from Cli import Cli
from Api import Api

parser = argparse.ArgumentParser()
parser.add_argument('port', type=int, nargs='?', default=4444)
args = parser.parse_args()

if __name__ == '__main__':
    serv = Serv(args.port)
    print("Started the node on " + serv.addr)
    api = Api(serv)
    cli = Cli(api)
    serv.start()
    cli.start()

'''
//Checklist
*# mesh network
*# join operation
*# New machines join the network by sending a join message to one of the machines already in the network.
*#    The address of the new host is thereupon propagated in the network.
*# Hosts also need to be able to sign off from the network again.
*# One node in the network needs to be elected as master node. The master node stores a
string variable that is initially empty.
*# Start message
*# The master node needs to be elected by the Bully algorithm.
*# In case the current master node signs off or fails a new master has to be elected.
*# The process takes 20 seconds. During this time all the nodes in the network do the
following: LOOP
    a) Wait a random amount of time
    b) Read the string variable from the master node
    c) Append some random english word to this string
    d) Write the updated string to the master node
    END LOOP
*# After the process has ended all the nodes read the final string from the master node and
write it to the screen.
*# Moreover they check if all the words they added to the string are
present in the final string. The result of this check is also written to the screen.
*# Ricart & Agrawala.
* All hosts have to write all the actions they perform to the screen in order to be able to
retrace the process.
'''