#!/usr/bin/env python
# encoding: utf-8
import unittest
from invitation import invitation as invitationINS

class InvitationTest(unittest.TestCase):

    def test_fun_inviteAnswerReplay(self):
        from player import Player
        from team import Team
        from player_manager import playerManager
        from team_manager import teamManager
        from draw_ import draw
        answer  = "Yes"
        inviter = Player()
        invitee = Player()
        localPlayer = Player()

        localPlayer.name = 'a'
        inviter.name='a'
        invitee.name='b'
        newTeam()





if __name__ == '__main__':
    unittest.main()


