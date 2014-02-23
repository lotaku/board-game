文件目录
    client
        client.py
        net.py
    server
        serve.rpy
        net.py
        player.py


#client.py

class Client:

    def __init__(self):
        #客户端数据

        self.init()

    def init(self):
        net.connectServer()

    def mainLoop(self):
        while True:
            #首先处理服务器发过来的网络，仅更新客户端数据
            net.handlePackets()

            #处理客户端事件，仅更新客户端数据
            self.handleEvents()

            #处理2步可能产生发给服务器的包
            #这里一起发送
            net.sendPackets()

            #更新客户端的这一frame的画面
            self.render()

client=Client()
client.mainLoop()

#client/net.py

#注意客户端面对的模型 一个自己对服务器
#服务器的模型是 一个服务器对多个客户端
def connectServer():
    pass

def handlePackets():
    packets=recvPackets()
    for packet in packet:
        packetId=packet.id
        handle[packetsId](packet)


def recvPackets():
    pass

def sendPackets():
    pass


#网络包理函数字典
handle={
    1:GS2CEnterWorld,
    2:GS2CPlayerMove,
}

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

    def packString(self,text)
        "压入字符串text,先压一个正数代表长度，然后压内容"
        self.addInt(len(text),size)
        #todo

    def send(self):
        send(self.buff) #todo

def GS2CEnterWorld(packet):
    "更新客户端数据"

def GS2CPlayerMove(packet):
    "更新客户端数据"

def C2GSEnterWorld():
    packet=Packet(1) #包的协议号
    packet.addString(name) #玩家名字
    packet.send()

def C2GSEnterWorld():
    packet=Packet(2) #包的协议号
    packet.addInt(x,1) #一个字节的正数代表x坐标
    packet.addInt(y,1) #
    packet.send()

#server/server.py

class Server:

    def init(self):
        net.beginServer()

    def mainLoop(self):
        while True:
            net.handleNetwork()

server=Server()
server.mainLoop()

#server/net.py

#注意客户端面对的模型 一个自己对服务器
#服务器的模型是 一个服务器对多个客户端

def beginListen():
    "开始监听"

def handlePackets()
    readables , writables , exceptionals = select.select(inputs, outputs, inputs, timeout)

    #某个特殊的input是服务器的监听socket

    for readable in readables:
        if readable is serverSocket:
            acceptConnect()
        else:
            data=readable.read()
            buffOfThisReadable+=data

            #tcp 分包
            buffOfPackets=parsePacket(buffOfThisReadable)

            player=playerManager.get(readable) #写个玩家管理类，
            #自己在acceptConnect()的时候把Player和readable关联起来

            for buffOfOnePacket in buffOfPackets:
                handle[buffOfPackets[0]](palyer,buffOfOnePacket)

handle={
    1:C2GSEnterWorld,
    2:C2GSPlayerMove,
}

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

    def packString(self,text)
        "压入字符串text,先压一个正数代表长度，然后压内容"
        self.addInt(len(text),size)
        #todo

    def send(self,player):
        #发送给单个玩家
        send(self.buff) #todo

    def send(self,players):
        #发送给单个玩家
        #todo

    def

def C2GSEnterWorld(player,buffer):
    #解包
    packet=RecvPacket(buff)
    name=packet.unpackStr()
    #验证请求合法性
    #修改服务器数据
    #通知客户端结果
    GS2CEnterWorld(player)

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
    packet.加个广播函数，广播世界内所有玩家()

#server/player

class Player:

    def __init__(self):
        self.name=""
        self.x
        self.y

    def move(self,newX,newY):
        pass

class PlayerManager:

    def add(self,player,socket):

    def del(self,socket)

    def get(self,socket)



