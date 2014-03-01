#!/usr/bin/env python
# encoding: utf-8
import player
handler={
    0:player.c2gsExitGame,
    1:player.c2gsEnterWorld,
    2:player.c2gsPlayerMove,
    6:player.c2gsTeamCreate
        }
def handlePacket(player,packet):
    handler[packet.id](player,packet)
