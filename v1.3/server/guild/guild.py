# encoding: utf-8
import marshal
from database import cursor
from player import playerManager

class CGuild:

    def __init__(self,name):
        self.m_Id=0
        self.m_Name=name
        self.m_Learder=''
        self.m_Members={} # id:player
        self.m_ApplyList=set() #
    def Add(self,player):
        self.m_Members[player.m_Id]=player
        GS2C


    def Load(self):
        sql = 'select data from tb_guild where id=%s'
        params=(self.m_Id,)
        cursor.execute(sql,params)
        data = cursor.fetchall()
        self.Unpack(data)

    def Save(self):
        data = self.Pack()
        sql = "update tb_guild set data=%s where id=%s"
        params = (data,self.m_Id)
        cursor.execute(sql,params)

    def Create(self):
        sql = "insert into tb_guild(id,data) values(%s,%s)"
        data = self.Pack()
        params = (self.m_Id,data)
        cursor.execute(sql,params)


    def ApplyEnterGuild(self,playerId,guildId):
        player=playerManager.Get(playerId)
        if not player:
            return #玩家已不存在

        if player.m_Guild:
            GS2CAlreadyInGuild(player)# 已在某个公会里
            return

        if self.m_ApplyList.get(player.m_Id,None):
            GS2CAlreadyApplyEnterGuild(player) #不要重复申请
            return

        guild = self.m_Guilds.get(guildId,None)
        if not guild:
            GS2CGuildNotExist(player) #公会已不存在

        guildLearder = playerManager.Get(guild.m_Learder)
        if not guildLearder:
            self.m_ApplyList.add(player)
            GS2CGuildLearderOffLine(player)#会长离线,等上线后处理,
            return

        GS2CApplyEnterGuild(player,guildLearder)#告诉会长,player申请进入工会


    def AgreeApplyEnterGuild(self,player,guildId):
        guild = self.m_Guilds[guildId]
        if guild.m_Members.get(player.m_Name,None):
            GS2CAlreadyInGuild()
            return

        guild.Add(player)
        guild.Save()
        #GS2CJoinGuildSuccess(player)

    def Pack(self):
        data ={'Id':self.m_Id,
               'Name':self.m_Name,
               'Learder':self.m_Learder,
               'Members':self.m_Members
               }
        return marshal.dumps(data)

    def Unpack(self,data):
        data =  marshal.loads(data)
        self.m_Id = data['Id']
        self.m_Name = data['Name']
        self.m_Learder= data['Learder']
        self.m_Members = data['Members']



