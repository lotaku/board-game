#!/usr/bin/env python
# encoding: utf-8
import player
handler={
    1:player.c2gsEnterWorld,
    2:player.c2gsPlayerMove,
    0:player.c2gsExitGame,
        }
def handlePacket(player,packet):
    handler[packet.id](player,packet)
