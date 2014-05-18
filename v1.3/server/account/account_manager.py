# encoding: utf-8

from account import Caccount
from login import GS2CNameRepeate
from login import GS2CLoginSuccess
from login import GS2CLoginInvaildName
from login import GS2CLoginInvaildPassword
from login import GS2CRegisteAccountSuccess
from login import GS2CChangePasswordSuccess
from login import GS2COldPasswordIncorrect
from player import CPlayer
from database import cursor

class CAccountManager:

    def __init__(self):
        self.m_MaxID=0
        self.m_Accounts={}
        self.m_NameAccount = {}

    def Add(self,account,newId=None):
        #为新玩家分配ID

        #更新当前服务器里玩家的最大ID 记录
        if newId is None:
            newId=self.m_MaxID
            self.m_MaxID +=1

        account.m_Id=newId


        self.m_Accounts[account.m_Id]=account
        self.m_NameAccount[account.m_Name]=account

    def Remove(self,account):
        if account.m_Id in self.m_Accounts:
            del self.m_Accounts[account.m_Id]
        if account.m_Name in self.m_NameAccount:
            del self.m_NameAccount[account.m_Name]

    def Get(self,Id):
        return self.m_Accounts.get(Id,None)

    def GetByName(self,name):
        account = self.m_NameAccount.get(name, None)
        if account:
            return account
        params=(name,)
        cursor.execute("select id,password from tb_account where name=%s",params)
        results=cursor.fetchall()
        if not results:
            return None
        name,password=results[0]

        account = Caccount(name,password)
        self.Add(account,account.m_ID)

        return account

    def RegisterAccount(self,socket,name,password):
        if self.GetByName(name):
            GS2CNameRepeate(socket)
            return
        account = Caccount(name,password)
        self.Add(account)

        sql = "insert into tb_account(id,name,password) values(%s,%s,%s)"
        params = (account.m_Id,name,password)
        cursor.execute(sql,params)
        GS2CRegisteAccountSuccess(socket,account)


    def LoginAccount(self,socket,name,password):
        account = self.GetByName(name)
        if not account :
            GS2CLoginInvaildName(socket)
            return

        if account.m_Password != password:
            GS2CLoginInvaildPassword(socket)
            return

        player=CPlayer()
        player.m_Account=account
        player.m_Socket=socket

        GS2CLoginSuccess(socket) # 以后发送已存在的玩家等信息

    def ChangePassword(self,socket,accountId,oldPassword,newPassword):
        account = self.Get(accountId)
        if oldPassword != account.m_Password:
            GS2COldPasswordIncorrect(socket)
            return
        account.m_Password=newPassword
        self.Add(account,account.m_Id)

        #from mylogger import log
        #log.info("login","% change password from %s to %s"%())
        sql = "update tb_account set password=%s where id=%s"
        params = (account.m_Password,account.m_Id)
        cursor.execute(sql,params)

        GS2CChangePasswordSuccess(socket)




#item/

    #goods.py

    #AllGoods={
            #1:{"name":"niunai","price":33432423}
            #2:{"name":"dangao","price":33432423}

    #}



if "accountManager" not in globals():
    accountManager = CAccountManager()

