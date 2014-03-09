#!/usr/bin/env python
# encoding: utf-8
import player
handler={
    0:player.c2gsExitGame,
    1:player.c2gsEnterWorld,
    2:player.c2gsPlayerMove,
    6:player.c2gsTeamCreate,
    8:player.c2gsInvited,
    9:player.c2gsInviteReplay,
    10:player.c2gsKickOut,
    11:player.c2gsTransferCaption,
        }
def handlePacket(player,packet):
    handler[packet.id](player,packet)
