#!/usr/bin/env python
# encoding: utf-8
from tcp_client import CTcpClient

class Client:

    def __init__(self):
        self.m_TcpClient = CTcpClient()


    def loop(self):
        while True:
            self.m_TcpClient.m_RecvData()


if '__main__' == __name__:

    client = Client()



#C2GSLogin=0x01

#1. zhuce
    #name        str
    #password    str

#2. login
    #name        str
    #password    str



#GS2CLogin=0x01

#1. RegisterResult,
    #result      4 byte int
    #errnor      1 byte int


#1.
