#!/usr/bin/env python
# encoding: utf-8
class Menu():
    def __init__(self):
        pass
    def createRightMenu(self):
        import player
        menuOption={
                0:("TeamCreat",player.localPlayer.c2gsTeamCreate),
                1:("Invited",player.localPlayer.c2gsInvited),
                2:("kickedOut",player.localPlayer.c2gsKickOut),
                3:("TransferCaptain",player.localPlayer.c2gsTransferCaptain),
                4:("JionIn",player.localPlayer.c2gsJoinIn),
                5:("QuitTeam",player.localPlayer.c2gsQuitTeam),
                6:("Disband","def6"),
                    }
        self.menuOption=menuOption
        self.menuOptionLength= len(menuOption)

        self.menuOptionList = []
        print menuOption
        for key, _ in menuOption.items():
            self.menuOptionList.append(key)


rightMenu = Menu()
rightMenu.createRightMenu()
