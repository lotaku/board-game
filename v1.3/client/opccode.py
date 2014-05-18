#!/usr/bin/env python
# encoding: utf-8

GS2CHandlerEnum = {
        1 : 'C2GS_TCP'
        }

GS2CHandlerSet = {
        'C2GS_TCP':'C2GSTcpHandler',

        }
def GS2CHandlerChoice(socket, packet):
    GS2CHandlerSet[GS2CHandlerEnum[packet.m_HandlerClassId]](socket, packet)



