#!/usr/bin/env python
# encoding: utf-8
class PlayerManager:
    def __init__(self):
        self.socketPlayer={}
        self.nameKVplayer={}
        self.players={}

    def add(self,player):
        self.socketPlayer[player.socket]=player
        self.nameKVplayer[player.name] = player
        self.players[player.name] = player

    def remove(self,player):
        del self.socketPlayer[player.socket]
    def get(self,socket):
        return self.socketPlayer[socket]
    def getPlayerByName(self,name):
        print "S端所有玩家实例：",self.players
        print "该函数的参数值 name：",name
        return self.players[name]

playerManager=PlayerManager()

