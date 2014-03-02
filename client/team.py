#!/usr/bin/env python
# encoding: utf-8
class Team():
    def __init__(self):
        self.caption = ''
        #self.name=""
        self.member=[]
    def create(self,player):
        self.caption = player.name
        self.name="TN"+player.name
        self.member.append(player.name)
        player.caption=1
        player.team=self
    def add(self,player):
        self.member.append(player)
    def remove(self,player):
        self.member.remove(player)
team=Team()

