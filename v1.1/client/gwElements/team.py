#!/usr/bin/env python
# encoding: utf-8
class Team():
    """
    创建一下新的队伍实例,不需要参数
    """
    def __init__(self):
        self.caption = ''
        self.member=[]
    def create(self,player):
        self.caption = player.name
        self.name="TN"+player.name
        self.member.append(player)
        player.team = self
    def add(self,player):
        if player not in self.member:
            self.member.append(player)
    def remove(self,player):
        self.member.remove(player)
    def removeByName(self,playerName):
        self.member.remove(playerName)
    def getPlayerByName(self,playerName):
        for playerArgm in self.member:
            if playerArgm.name == playerName:
                return playerArgm
            else:
                print "该玩家不存在，请确认玩家的名字正确（str型）"

