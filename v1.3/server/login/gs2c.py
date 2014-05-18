# encoding: utf-8
from packet import CSendPacket
from opccode import *

def GS2CNameRepeate(socket):
    packet = CSendPacket(GS2C_LOGIN,1)
    packet.PackString(name)
    packet.Send()

def GS2CRegisteAccountSuccess(socket, account):
    packet = CSendPacket(GS2C_LOGIN,2)
    packet.PackString()

def GS2CLoginInvaildName(socket,name):
    packet =  CSendPacket(GS2C_LOGIN,3)
    packet.PackString(name)

def GS2COldPasswordIncorrect(socket):
    packet=CSendPacket(GS2C_LOGIN,4)
    packet.SendToSocket(socket)


def GS2CChangePasswordSuccess(socket):
    packet=CSendPacket(GS2C_LOGIN,5)
    packet.SendToSocket(socket)




