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
        try:
            return self.teams[player.team.name]
        except:
            return None

teamManager = TeamManager()
