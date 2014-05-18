# encoding: utf-8
from account import accountManager

def C2GSRegisterAccount(socket,packet):
    name=packet.UnpackString()
    password=packet.UnpackString()
    accountManager.RegisterAccount(socket,name,password)


def C2GSLoginAccount(socket,packet):
    name=packet.UnpackString()
    password=packet.UnpackString()
    accountManager.LoginAccount(socket,name,password)

def C2GSChangePassword(socket,packet):
    accountId=packet.UnPackInt()
    oldPassword=packet.UnPackString()
    newPassword=packet.UnpackString()
    accountManager.ChangePassword(socket, accountId,oldPassword,newPassword)


Handler={
    1:C2GSRegisterAccount,
    2:C2GSLoginAccount,
}

def C2GSLoginHandler(remoteSocket,packet):
    Handler[packet.m_HandlerId](remoteSocket,packet)

