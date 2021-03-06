#!/usr/bin/env python
# encoding: utf-8
class PlayerManager:
    def __init__(self):
        self.remotePlayers={}
    def add(self,player):
        self.remotePlayers[player.name]=player
    def remove(self,player):
        del self.remotePlayers[player.name]
    def get(self,name):
        player = self.remotePlayers[name]
        return player

playerManager=PlayerManager()
