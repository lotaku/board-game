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
        #print 'teamManager_11行:玩家队伍名',player.team
        #print "当teamManager_12行:右键下玩家的名字",player.name
        #print "当teamManager_13行:前所有队伍",self.teams
        try:
            return self.teams[player.team]
        except KeyError:
            print "该玩家没有加入任何队伍"
            return None

teamManager = TeamManager()
