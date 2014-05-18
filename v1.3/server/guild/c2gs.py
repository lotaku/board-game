#!/usr/bin/env python
# encoding: utf-8
from guild_manager import guildManager
#from player import playerManager

def C2GSCreateGuild(player,packet):
    name=packet.UnPackString()
    guildManager.CreateGuild(player,name)

def C2GSApplyGuild(player,packet):
    guildId= packet.UnPackInt()
    guild=guildManager.Get(guildId)
    guild.ApplyEnterGuild(player)

def C2GSAgreeApplyEnterGuild(guildLearder,packet):
    newMemberId=packet.UnPackInt()
    guildId = packet.UnPackInt()
    guild = guildManager.Get(guildId)
    guild.Add(newMemberId)

#def C2GSApplyEnterGuild(player,packet):
    #guilId= packet.UnPackInt()
    #guildManager.ApplyEnterGuild(player,guilId)
