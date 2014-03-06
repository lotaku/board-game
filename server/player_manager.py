#!/usr/bin/env python
# encoding: utf-8
class PlayerManager:
    def __init__(self):
        self.socketPlayer={}
        self.nameKVplayer={}

    def add(self,player):
        self.socketPlayer[player.socket]=player
        self.nameKVplayer[player.name] = player

    def remove(self,player):
        del self.socketPlayer[player.socket]
    def get(self,socket):
        return self.socketPlayer[socket]
    def getPlayerByName(self,name):
        return self.nameKVplayer[name]

playerManager=PlayerManager()

