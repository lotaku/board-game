board-game
==========

棋盘游戏（学习中......）

#2014-03-09 16:12:28

实现 踢出队友,但每次 '踢出后,',需要重新修改玩家的右键弹出菜单

#2014-02-24 15:58:06

为了让服务器S 的select 知道 玩家player已经退出游戏
    1. 增加player.exitKey = 0 
在 S 压包同时其他客户端时， 修改：player.exitKey = 1,
S 的 select 在 write 后，判断 player.exitKey ,为真时，将 player从 待写的 socket 中移除，删除玩家在playerManaer里的记录

#2014-02-15 14:47:25

![多人游戏](https://raw2.github.com/lotaku/board-game/master/img/demo_1.1.png)

#2014-02-11 13:20:49
游戏窗口图片：
![女孩移动](https://raw2.github.com/lotaku/board-game/master/img/demo_1.0.png)





