#!/usr/bin/env python
# encoding: utf-8
import player
#from player import Player
#x2=player.Player()
#print "创建玩家实例：x2",x2
handler={
    0:player.gs2cOtherExitGame,
    1:player.gs2cEnterWorld,
    2:player.gs2cPlayerMove,
    3:player.gs2cOtherEnterWorld,
    4:player.gs2cOtherMove,
    5:player.gs2cExistingPlayers,
    6:player.gs2cTeamCreate,
    7:player.gs2cOtherTeamCreate,
    8:player.gs2cInviteAsk,
    9:player.gs2cInviteReply,
    10:player.gs2cKickOut,
    11:player.gs2cTransferCaptain,
    12:player.gs2cJoinIn,
    13:player.gs2cQuitTeam,

        }

def handlePacket(packet):
    handler[packet.id](player.localPlayer,packet)

