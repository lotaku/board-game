#!/usr/bin/env python
# encoding: utf-8
class TeamManager():
    def __init__(self):
        self.teams={}
    def add(self,team):
        self.teams[team.name]=team
        print "新队伍加入:", team.name
        print "所有队伍:",self.teams
    def remove(self,team):
        del self.teams[team.name]
    def get(self,player):
        try:
            return self.teams[player.team]
        except KeyError:
            print "玩家队伍的名字:期待一个str name:",player.team
            print "team_manager.py:19line :该玩家没有加入任何队伍"
            return None

    def getByTeamName(self,player):
        try:
            return self.teams[player.teamName]
        except KeyError:
            print "玩家队伍的名字:期待一个str name:",player.teamName
            print "team_manager.py:19line :该玩家没有加入任何队伍"
            return None
teamManager = TeamManager()
