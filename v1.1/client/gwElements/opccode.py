#!/usr/bin/env python
# encoding: utf-8
#import player
import player_gs2c

handler={
    0:player_gs2c.gs2cOtherExitGame,
    1:player_gs2c.gs2cEnterWorld,
    2:player_gs2c.gs2cPlayerMove,
    3:player_gs2c.gs2cOtherEnterWorld,
    4:player_gs2c.gs2cOtherMove,
    5:player_gs2c.gs2cExistingPlayers,
    6:player_gs2c.gs2cTeamCreate,
    7:player_gs2c.gs2cOtherTeamCreate,
    8:player_gs2c.gs2cInviteAsk,
    9:player_gs2c.gs2cInviteReply,
    10:player_gs2c.gs2cKickOut,
    11:player_gs2c.gs2cTransferCaptain,
    12:player_gs2c.gs2cJoinIn,
    13:player_gs2c.gs2cQuitTeam,

        }

def handlePacket(packet):
    from player import localPlayer
    handler[packet.id](localPlayer,packet)

