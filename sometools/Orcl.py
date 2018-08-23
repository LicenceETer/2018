#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cx_Oracle as cx
import time

Source_databse_info ={
    'user': 'c##test01',
    'password': 'test01',
}
#连接远端数据库请使用TNS方法进行连接，TNS文件位于$ORACLE_HOME//network/admin/tnsnames.ora
#信息填写格式如下
#Source_databse_info=("USERNAME/PASSWORD@127.0.0.1/SERVICE_NAME")
#具体可查阅文档 https://cx-oracle.readthedocs.io/en/latest/module.html cx_Oracle.connet类的使用方法

Dest_database_info = {
    'user': 'c##test01',
    'password': 'test01',
}


def connect_database():
    #数据库连接函数，返回源数据库和目标数据库的光标对象、连接对象
    try:
        print('正在连接源数据库...')
        global  Source_conn     #将connet变量全局化，便于最后Source_conn.close()
        Source_conn = cx.connect(**Source_databse_info)
        print('连接成功！')
        print('源数据库版本是：%s \n' % Source_conn.version )
    except:
        print('连接失败，请检查数据库信息是否正确。')
        os._exit(0)     #若无法连接，退出脚本
    try:
        print('正在连接目标数据库...')
        global Dst_conn     #将connet变量全局化，便于最后Dst_conn.close()
        Dst_conn = cx.connect(**Dest_database_info)
        print('连接成功！')
        print('目标数据库版本是：%s \n' % Dst_conn.version)
    except :
        print('连接失败，请检查数据库信息是否正确。')
        os._exit(0)     #若无法连接，退出脚本
    global Source_cur       #将光标变量全局化，便于其他函数调用
    Source_cur = Source_conn.cursor()
    global Dst_cur
    Dst_cur = Dst_conn.cursor()

    return Source_cur,Dst_cur,Source_conn,Dst_conn
    pass

def get_database_list(cur):
    #获取所有数据库名，返回数据库列表
    sql = 'select name from v$database'
    result = cur.execute(sql)   #得到的result是一个元组
    database_list = list(map(lambda x: x[0], result))   #转换成列表
    return database_list

def get_database_name(tips,database_list):
    #列出数据库名称，返回所选择的数据库名
    print(tips)
    for i in range(len(database_list)):
        print(str(i + 1) + ':' + database_list[i], end='\t')
    database_name = database_list[int(input('\n')) - 1]
    print('\n')
    return database_name
    pass

def get_table_list(cur):
    #列出该用户下的所有表名，并返回选中的表名
    sql = 'select table_name from user_tables'
    result = cur.execute(sql)
    table_list = list(map(lambda x: x[0], result))
    print('请选择要同步的表（输入序号）：')
    for i in range(len(table_list)):
        print('['+str(i + 1)+']'+table_list[i],end='\n')
    table_name = table_list[int(input('\n')) - 1]
    return table_name

def copy_table_struct(Source_table_name,Dst_table_name):
    #获取表中所有column_name，拼凑CREATE TABEL语句
    sql_get_column_name = 'select COLUMN_NAME,DATA_TYPE,DATA_LENGTH from user_tab_columns where Table_name=\'%s\'' % Source_table_name
    Source_cur.execute(sql_get_column_name)
    Source_column_name = Source_cur.fetchall()
    #print(Source_column_name)
    print('正在复制表结构\n')

    try:
        #这里拼凑CREATE TABEL的语句
        sql_create_tabel = 'create TABLE %s(\n' % Dst_table_name
        for i in range(len(Source_column_name)-1):
            sql_create_tabel = sql_create_tabel + '%s %s(%d),\n' % (Source_column_name[i][0],Source_column_name[i][1],Source_column_name[i][2])
        sql_create_tabel = sql_create_tabel + '%s %s(%d) \n' % (Source_column_name[-1][0],Source_column_name[-1][1],Source_column_name[-1][2])
        sql_create_tabel = sql_create_tabel + ')'
    except:
        print('Error! 表结构创建失败  \n')
        os._exit(0)

    #print(sql_create_tabel)
    Dst_cur.execute(str(sql_create_tabel))  #在目的数据库中执行
    print('表结构复制成功\n')

def copy_table_data(Source_table_name,Dst_table_name,):
    sql_get_column_name = 'select COLUMN_NAME from user_tab_columns where Table_name=\'%s\'' % Source_table_name
    Source_cur.execute(sql_get_column_name)
    Source_column_name = Source_cur.fetchall()
    sql_copy_data_p1 = 'INSERT INTO %s(' % Dst_table_name
    for i in range(len(Source_column_name)-1):
        sql_copy_data_p1 = sql_copy_data_p1 + '%s,' % Source_column_name[i]
    sql_copy_data_p1 = sql_copy_data_p1 + '%s)' % Source_column_name[-1]
    #拼凑INSERT INTO的第一部分语句:INSERT INTO TABLE_NAME ('COLUMN_NAME1','COLUMN_NAME2'......)
    print('正在复制数据...\n')
    Source_cur.execute('select count(*) from %s' % Source_table_name)
    count = Source_cur.fetchone()   #得到数据数量

    Source_cur.execute('select * from %s' % Source_table_name)
    for i in range(int(count[0])):
        data = Source_cur.fetchone()
        sql_copy_data_p2 = sql_copy_data_p1 + 'VALUES('
        for j in range(len(data) - 1):
            if data[j] == None :
                sql_copy_data_p2 = sql_copy_data_p2 + 'Null,'
            else:
                sql_copy_data_p2 = sql_copy_data_p2 + '\'%s\',' % data[j]
        if data[-1] == None :
            sql_copy_data_p2 = sql_copy_data_p2 + 'Null)'
        else:
            sql_copy_data_p2 = sql_copy_data_p2 + '\'%s\')' % data[-1]
        #拼凑INSERT INTO的第二部分语句 VALUES('VALUE1','VALUE2',........)
        #为防止吃掉所有内存，这里使用一行数据一条语句的方式进行操作，当数据量特别大的时候考虑使用多线程
        Dst_cur.execute(str(sql_copy_data_p2))  #执行语句
    Dst_conn.commit()

def confirm(Source_database_name,Source_table_name,Dst_database_name,Dst_table_name):
    print('即将开始复制，请确认信息是否正确\n')
    print('源数据库是：%s  源表是：%s \n' % (Source_database_name,Source_table_name))
    print('目标数据库是：%s    目标表是：%s \n' % (Dst_database_name,Dst_table_name))
    rst = str(input('是否继续？ y/n \n' ))
    return rst

def run():
    try:
        connect_database()
        Source_database_list = get_database_list(Source_cur)
        Source_database_name = get_database_name('请输入源数据库(输入序号):',Source_database_list)
        Dst_database_list = get_database_list(Dst_cur)
        Dst_database_name = get_database_name('请输入目标数据库(输入序号):',Dst_database_list)
        #print(Source_database_name)
        #print(Dst_database_name)
        Source_table_name = get_table_list(Source_cur)
        print('你选中的表是：%s \n' % Source_table_name)
        Dst_table_name = str(input('请输入新的表名:\n'))
        print(Dst_table_name+'\n')
        rst=confirm(Source_database_name,Source_table_name,Dst_database_name,Dst_table_name)
        if rst=='y' or rst == 'Y':
            copy_table_struct(Source_table_name,Dst_table_name)
            copy_table_data(Source_table_name,Dst_table_name)
        else:
            print('操作已取消')
            os._exit(0)
        print('复制成功！\n')
    finally:
        Source_conn.close()
        Dst_conn.close()
run()
