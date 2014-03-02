#!/usr/bin/env python
# encoding: utf-8
class TeamManager():
    def __init__(self):
        self.teams={}
    def add(self,team):
        self.teams[team.name]=team
    def remove(self,team):
        del self.teams[team.name]
    def get(self,player):
        print '玩家队伍名',player.team
        if player.team:
            return self.teams[player.team]
        else:
            return None
        #if self.teams[player.team]:

teamManager = TeamManager()
