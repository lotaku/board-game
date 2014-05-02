

class CTeam:

	def __init__(self,...):
		self.m_MemberList=[]
		self.m_InviteList=[]


	def AddMember(self,who):
		self.m_MemberList.append(who.m_ID)

		GS2CJoinTeam(who,self) #通知who他进入self这个队伍

		GS2CNewMenber(self,who) #通知队伍内其他人，who进入了队伍

