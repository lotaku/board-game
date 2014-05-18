#!/usr/bin/env python
# encoding: utf-8
from database import cursor
from guild import CGuild
from guild import GS2CGuildNameRepeat
from guild import GS2CAlreadyInGuild
from player import playerManager
class CGuildManager:

    def __init__(self):
        self.m_Guilds={} # id : Guild
        self.m_NameGuild={}
        self.m_MaxID =1

    def Add(self,guild,newId=None):
        if newId is None:
            newId=self.m_MaxID
            self.m_MaxID +=1

        guild.m_Id = newId

        self.m_Guilds[guild.m_Id]=guild
        self.m_NameGuild[guild.m_Name]=guild


    def CreateGuild(self,player,name):
        #to判断名字的合法性
        guild =  self.GetByName(name)
        if guild:
            GS2CGuildNameRepeat(player)
            return
        results = self.SQLNameExist(name)
        if results:
            GS2CGuildNameRepeat(player)
            return

        guild=CGuild(name)

        self.Add(guild)

        guild.Create()

    def Get(self,id): #return Guild
        return self.m_Guilds.get(id, None)

    def GetByName(self,name):

        guild= self.m_NameGuild.get(name, None)
        if guild:
            return guild

    def SQLNameExist(self,player,name):
        sql = 'select id from tb_guild where name=%s'
        params=(name,)
        cursor.execute(sql,params)
        results =cursor.fetchall()
        if not results:
            return GS2CGuildNameRepeat(player)
        return results



guildManager=CGuildManager()

