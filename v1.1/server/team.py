#!/usr/bin/env python
# encoding: utf-8
class Team():
    def __init__(self):
        self.member=[]
        self.caption= ''
    def create(self,player):
        self.caption = player.name
        self.name="TN"+player.name
        self.add(player)
    def add(self,player):
        self.member.append(player)
    def remove(self,player):
        self.member.remove(player)
team=Team()
