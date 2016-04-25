import random
from xmlrpc.client import ServerProxy
import socket

words = open('top.txt').read().splitlines()


def get_random_word():
    word =random.choice(words)
    return word

def get_node_by_addr(addr):
    return ServerProxy('http://' + addr).Api
