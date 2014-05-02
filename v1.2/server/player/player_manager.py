#!/usr/bin/env python
# encoding: utf-8
class CPlayerManager:
    def __init__(self):
        self.m_MaxID=0
        self.m_Players={}


    def Add(self,who):
        #为新玩家分配ID
        who.m_Id=self.m_MaxID+1

        #更新当前服务器里玩家的最大ID 记录
        self.m_MaxID +=1

        self.m_Players[who.m_Id]=who

    def Remove(self,who):
        self.m_Players.popitem(who.m_Id)

    def Get(self,m_Id):
        return self.m_Players[m_Id]

playerManager = CPlayerManager()
