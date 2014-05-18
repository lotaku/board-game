# encoding: utf-8

class CRecvPacket:

    def __init__(self, buffer):
        self.m_HandlerClassId=ord(buffer[0])
        self.m_HandlerId=ord(buffer[1])
        self.m_Buffer=buffer
        self.m_CurrentIndex=2

    def UnPackInt(self):
        pass

class CSendPacket:

    def __init__(self,m_HandlerClassId, m_HandlerId):
        #self.m_HandlerClassId=m_HandlerClassId
        #self.m_HandlerId= m_HandlerId
        self.m_Buffer=chr(m_HandlerClassId)
        self.m_Buffer += chr(m_HandlerId)

    def PackInt(self, value):
        self.m_Buffer +=chr(value/0x100)+chr(value%0x100)

    def PackString(self, text):
        length = len(text)
        self.PackInt(length)
        self.m_Buffer+=text

    def Send(self):
        length = len(self.m_Buffer)
        buffer=chr(length/0x100) + chr(length%0x100) + self.m_Buffer
        tcpClient.m_SendData += buffer






