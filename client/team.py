#!/usr/bin/env python
# encoding: utf-8
class Team():
    """
    创建一下新的队伍实例,不需要参数
    """
    def __init__(self):
        self.caption = ''
        #self.name=""
        self.member=[]
    def create(self,player):
        self.caption = player.name
        self.name="TN"+player.name
        self.member.append(player.name)
        #修改:下面的,不要在这里关联,team 只做team的事情
        #player.iscaption=1
        #player.team=self
    def add(self,playerName):
        if playerName not in self.member:
            self.member.append(playerName)
    def remove(self,player):
        self.member.remove(player)
team=Team()

