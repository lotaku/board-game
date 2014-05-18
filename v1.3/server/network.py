# encoding: utf-8

from opccode import *
from login import C2GSLoginHandler
from team import C2GSTeamHandler
from friend import C2GSFriendHandler
C2GSTcpHandler = {
    C2GS_LOGIN:C2GSLoginHandler,
    C2GS_TEAM:C2GSTeamHandler,
    C2GS_FRIEND:C2GSFriendHandler,
}


