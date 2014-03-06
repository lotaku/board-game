#!/usr/bin/env python
# encoding: utf-8
import player
import team
#import player as playerM
handler={
    #1:playerM.gs2cEnterWorld,
    #2:playerM.gs2cPlayerMove,
    #1:player.player.gs2cEnterWorld,
    #2:player.player.gs2cPlayerMove,
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

        }

def handlePacket(packet):
    #handler[packet.id](playerM.player,packet)
    handler[packet.id](player.player,packet)

