#!/usr/bin/env python
# encoding: utf-8
class PlayerManager:
    def __init__(self):
        self.players={}
    def add(self,player):
        self.players[player.name]=player
    def remove(self,player):
        del self.players[player.name]
    def getPlayerByName(self,name):
        player = self.players[name]
        return player

playerManager=PlayerManager()
