#!/usr/bin/env python
# encoding: utf-8
import player
#from player import player

#import player as playerM
handler={
    #1:playerM.gs2cEnterWorld,
    #2:playerM.gs2cPlayerMove,
    #1:player.player.gs2cEnterWorld,
    #2:player.player.gs2cPlayerMove,
    1:player.gs2cEnterWorld,
    2:player.gs2cPlayerMove,
        }

def handlePacket(packet):
    #handler[packet.id](playerM.player,packet)
    handler[packet.id](player.player,packet)

