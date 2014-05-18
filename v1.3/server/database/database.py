# -*- coding: utf-8 -*-
#mysqldb
import time, MySQLdb

#连接
conn=MySQLdb.connect(host="localhost",user="root",passwd="123qwe",db="db_game",charset="utf8")
cursor = conn.cursor()

#写入
sql = "insert into tb_account(id,name,password) values(%s,%s,%s)"
param = ('1','Lili','123qwe')
n = cursor.execute(sql,param)
print n

#更新
sql = "update tb_account set name=%s where id=1"
param = ("name2",)
n = cursor.execute(sql,param)
print n

#查询
n = cursor.execute("select name,password from tb_account where id=1")
for row in cursor.fetchall():
    print row

#查询
params=("name2",)
n = cursor.execute("select id,password from tb_account where name=%s",params)
print cursor.fetchall()
##删除
#sql = "delete from user where name=%s"
#param =("aaa")
#n = cursor.execute(sql,param)
#print n
cursor.close()

#关闭
conn.close()
