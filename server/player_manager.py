#!/usr/bin/env python
# encoding: utf-8
class PlayerManager:
    def __init__(self):
        self.socketPlayer={}

    def add(self,player):
        self.socketPlayer[player.socket]=player

    def remove(self,player):
        del self.socketPlayer[player.socket]
    def get(self,socket):
        return self.socketPlayer[socket]

playerManager=PlayerManager()

