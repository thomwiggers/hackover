#!/usr/bin/env python2
from __future__ import print_function
# Insecure Shell 2 hacker - Hackover 2016
# Thom Wiggers <thom@thomwiggers.nl>

import socket
import os
from binascii import hexlify
import struct


def send(s, data):
    try:
        s.send(struct.pack('!h', len(data)))
        s.send(data)
    except:
        os.kill(os.getpid(), 9)


def recv(s):
    try:
        l = struct.unpack('!h', s.recv(2))[0]
        data = s.recv(l)
    except:
        os.kill(os.getpid(), 9)
    return data


def connect(host, port):
    nonce_len = len("Nonce:") + 32
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(1)
    s.connect((host, port))
    t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    t.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    t.setblocking(1)
    t.connect((host, port))
    print("connected")
    # no longer needed to do this
    nonce = "Nonce:;echo hi;                       "
    assert len(nonce) == nonce_len, "{} != {}".format(len(nonce), nonce_len)
    print("Sending challenge")
    print("challenge: %s" % nonce)
    send(s, nonce)
    enccmd = recv(s)
    print("Encrypted response: {}".format(hexlify(enccmd)))
    send(s, "ok")
    challenge = recv(s)
    print("Being challenged by s: {}".format(challenge))
    print("Sending challenge to t")
    send(t, challenge)
    encnonce = recv(t)
    print("Getting response from t {}".format(hexlify(encnonce)))
    print("Sending response from t to s")
    send(s, encnonce)
    print("We should now get ok")
    okmsg = recv(s)
    assert okmsg == "ok"
    print("We got ok")
    print("Sending commands to s")
    send(s, "get-flag")
    print(recv(s))


if __name__ == "__main__":
    print("client")
    connect("challenges.hackover.h4q.it", 40804)
    # connect('localhost', 40804)
