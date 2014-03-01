#!/usr/bin/env python
# encoding: utf-8
class PlayerManager:
    def __init__(self):
        self.remotePlayers={}
        #self.remotePlayers=[]
    def add(self,player):
        self.remotePlayers[player.name]=player
        #self.remotePlayers.append(player)
    def remove(self,player):
        #self.remotePlayers.remove(player)
        del self.remotePlayers[player.name]
    def get(self,name):
        player = self.remotePlayers[name]
        return player

playerManager=PlayerManager()
