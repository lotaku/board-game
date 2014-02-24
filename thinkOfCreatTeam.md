##要求：
1,建立队伍，邀请加入，申请加入，接受拒绝 ，解散队伍。
2。踢人
3,转队长
4,设计一套 协议  ，包的内容 。作用，什么时间发，期待回什么。
5,画个队员列表。

！首先设计一套协议包。

## 尝试协议包设计
1,C 建立队伍：


    C 发6号包  -->  内容：player.name

    S 回6号包  -->  内容：player.name
        S 新建一个 队伍类,          newTeam = TeamCreat(player)
                                        -->newTeam.name= 由玩家输入
                                        -->newTeam.caption=player
                                        -->newTeam.member=[]
                                        -->player.team = newTeam.name
        S 新建一个 队伍管理 类,     teamManager = TeamManager()
                                    teamManager.add(newTeam) # 结构 --> {newTeam.name : newTeam}

    C 接6号包  --> 获得 player.name
        C 新建一个 队伍类，         newTeam = TeamCreat(Player)
                                        -->newTeam.caption=player
                                        -->newTeam.member=[]
        S 新建一个 队伍管理 类,     teamManager = TeamManager()
                                    teamManager.add(newTeam) # 结构 --> {newTeam.name : newTeam}
2,C 邀请加入:


    C 发7号包  -->  内容：player.name,  invitedPlayer.name
    S 回7号包,发送给 invitedPlayer -->  内容：player.name,  invitedPlayer.name
            询问 是否同意加入 player 的队伍
    C(invitedPlayer)收到 7号，发 8 号给 S --> 内容： 是否同意1,0,  player.name, invitedPlayer.name
            若同意，S 发8号包 --> 更新 player的队伍成员信息，并广播所有玩家
            若拒绝，S 发8号包 --> 通知 player 结果

    C 接8号包 -->
        若收到 数字 0 ，提示玩家拒绝加入
        若收到 数字 1  ，提示玩家同意邀请，更新本地队伍信息

3,C 踢人：


    C 发9号包 --> 包内容：player.name, memberPlayer.name
        S 接9号包 --> 更新player.team 的成员信息
        S 发9号包 --> (包内容：广播）player.name,memberPlayer, #由player.name-->player类-->player.team-->team.remove(memberPlayer)
    C 接9号包 --> 更新队伍信息

4,转队长：


    C 发10号包 --> 包内容：player.name(队长), memberPlayer.name(队员)
        S接10号包--发10号包给 memberPlayer
    C(memberPlayer)--发11号包 -->
        若同意，S 更新服务器队伍信息，发 11号包(广播) --> 包内容：player.name(队长),memberPlayer.name(队员)  # 通过队长获得 “队伍” team，team.caption = memberPlayer
        若决绝，S 发11号包给 C（player.name),不更新组信息，也不用广播









