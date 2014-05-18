#!/usr/bin/env python
# encoding: utf-8
from tcp_server import CTcpServer

if '__main__' == __name__:
    tcpServer = CTcpServer()
    tcpServer.Listen()
    tcpServer.Run()
