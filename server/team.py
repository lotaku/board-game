#!/usr/bin/env python
# encoding: utf-8
class Team():
    def __init__(self):
        self.member=[]
    def create(self,player):
        self.caption = player.name
        self.name="TN"+player.name
        player.team=self # 可以这样?意义:队长和所在队伍关联
    def add(self,player):
        self.member.append(player)
    def remove(self,player):
        self.member.remove(player)
team=Team()
