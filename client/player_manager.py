#!/usr/bin/env python
# encoding: utf-8
class PlayerManager:
    def __init__(self):
        #self.remotePlayers={}
        self.remotePlayers=[]
    def add(self,player):
        #name = player.name
        #self.remotePlayers[name]=player
        self.remotePlayers.append(player)
    def remove(self,player):
        #self.remotePlayers.remove(player)
        self.remotePlayers.remove(player)

playerManager=PlayerManager()
