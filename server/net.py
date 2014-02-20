#!/usr/bin/env python
# encoding: utf-8
#server/net.py
import socket
import player
import Queue
import select
userInWorld = {}
serverSocket =None
#A optional parameter for select is TIMEOUT
#初始化 playerManager
playerManager = player.PlayerManager()
#注意客户端面对的模型 一个自己对服务器
#服务器的模型是 一个服务器对多个客户端

class RecvPacket:
    def __init__(self,buff):
        self.buff=buff
        self.currentIndex=0

    def unpackInt(self,size):
        return int

    def unpackStr(self):
        return str

class SendPacket:
    def __init__(self):
        self.buffer=""

    def packInt(self,value,size):
        "压入一个size字节的整数value"

    def packString(self,text):
        "压入字符串text,先压一个正数代表长度，然后压内容"
        self.addInt(len(text),size)
        #todo
    #def send(self,player):
        ##发送给单个玩家
        #send(self.buff) #todo

    def send(self,players):
        #发送给单个玩家
        #todo
        pass
def C2GSEnterWorld(player,buffer,readable):
        ##解包
    player.name = buffer[1]
    player.x = buffer[2]
    player.y = buffer[3]
    print player.name
    print player.x
    print player.y
    readable.sent('xxx')

    #packet=RecvPacket(buff)
    #name=packet.unpackStr()
    ##验证请求合法性
    ##修改服务器数据
    ##通知客户端结果
    #GS2CEnterWorld(player)


def GS2CEnterWorld(player):
    packet=Packet(1) #包的协议号
    packet.addInt(x,1) #一个字节的正数代表x坐标
    packet.addInt(y,1) #
    packet.send()

def C2GSPlayerMove(player,buffer):
    #解包
    packet=RecvPacket(buff)
    x=packet.unpackInt(1)
    y=packet.unpackInt(1)
    #验证请求合法性
    #修改服务器数据
    #通知客户端结果
    GS2CPlayerMove(player)

def GS2CPlayer(player):
    packet=Packet(y) #包的协议号
    packet.addInt(player.x,1) #一个字节的正数代表x坐标
    packet.addInt(player.y,1) #
    #packet.加个广播函数，广播世界内所有玩家()


def beginListen():
    global serverSocket
    """
    开始监听
    """
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.setblocking(0)
    serverAddress = ('', 51423)
    serverSocket.bind(serverAddress)
    serverSocket.listen(10)

def handlePackets():
    global serverSocket
    inputs = [serverSocket]
    outputs = []
    exceptionals = []
    timeout = 20
    message_queues = {}
    while inputs :
        print 'waiting for next event:'
        readables, writables, exceptionals = select.select(inputs, outputs,inputs, timeout)
        if not (readables or writables or exceptionals):
            print 'time out'
        for readable in readables :
            if readable is serverSocket :
                #A "readable" socket is ready to accept a connect a connection
                client_socket, client_address = readable.accept()
                print ' connect from ', client_address
                client_socket.setblocking(0)
                inputs.append(client_socket)
                message_queues[client_socket] = Queue.Queue()
            else:
                data = readable.recv(1024)
                if data :
                    print 'received ', data , 'from ', readable.getpeername()
                    message_queues[readable].put(data)
                    if readable not in outputs :
                        outputs.append(readable)
                else:
                    print 'closing ,', client_address
                    if readable in outputs :
                        outputs.remove(readable)
                    inputs.remove(readable)
                    readable.close()
                    del message_queues[readable]
        for writable in writables :
            try :
                next_msg = message_queues[writable].get_nowait()
            except Queue.Empty :
                print ' ', writable.getpeername(), 'queue empty'
                outputs.remove(writable)
            else:
                print ' sending ', next_msg, ' to ', writable.getpeername()
                writable.send(next_msg)
        for exceptional in exceptionals :
            print ' exceptional condition on ', exceptional.getpeername()
            inputs.remove(exceptional)
            if exceptional in outputs :
                outputs.remove(exceptional)
            exceptional.close()
            del message_queues[exceptional]


handle={
    1:C2GSEnterWorld,
    2:C2GSPlayerMove,
}
