

def C2GSCreateTeam(who):
	if hasattr(who,"m_Team"):
		GS2CCreateTeamFail(who)
		return

	unpack create team args
	teamObj=CTeam(create team args)
	teamObj.AddMember(who)
	teamObj.SetOwner(who)


	who.m_Team=teamObj

	GS2CCreateTeamSuccess(who)

def C2GSAcceptTeamInvite(who):
	fromPid=UnpackInt() # from pid 邀请 who加入他的队伍

	fromPlayer=GetPlayer(fromPid)
	if not hasattr(fromPlayer,"m_Team"):
		#发出邀请的玩家已经离开队伍，邀请无效
		return

	if who.m_ID not in fromPlayre.m_Team.m_InviteList:
		#这个玩家并没有被这个队伍邀请，这个非法请求
		return

	#继续判断其他可能的非法情况


	#确认合法以后

	#把玩家加入到队伍里面

	fromPlayer.m_Team.AddMember(who)

C2GSTeamHandler={
	1:C2GSCreateTeam,
	2:C2GSAcceptTeamInvite,
}
