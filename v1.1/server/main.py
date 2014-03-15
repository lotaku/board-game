#!/usr/bin/env python
# encoding: utf-8
from tcp_server import TcpServer


tcpServer=TcpServer()
tcpServer.listen()
tcpServer.run()
