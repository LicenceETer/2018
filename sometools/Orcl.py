#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cx_Oracle as cx
import time

Source_databse_info = {
    'user': 'c##test01',
    'password': 'test01',
}

Dest_database_info = {
    'user': 'c##test01',
    'password': 'test01',
}

def connect_database():
    try:
        global  Source_conn     #将connet变量全局化，便于最后Source_conn.close()
        Source_conn = cx.connect(**Source_databse_info)
    except:
        print('Connect to Source Databse Failed , Please Check Connection Info')
        os._exit(0)     #若无法连接，退出脚本
    try:
        global Dst_conn     #将connet变量全局化，便于最后Dst_conn.close()
        Dst_conn = cx.connect(**Dest_database_info)
    except :
        print('Connect to Destination Databse Failed , Please Check Connection Info')
        os._exit(0)     #若无法连接，退出脚本
    global Source_cur       #将光标变量全局化，便于其他函数调用
    Source_cur = Source_conn.cursor()
    global Dst_cur
    Dst_cur = Dst_conn.cursor()
    print('The Source Database version is '+ Source_conn.version )
    print('The Destination Database version is ' + Dst_conn.version)
    return Source_cur,Dst_cur,Source_conn,Dst_conn
    pass

def get_database_list(cur):
    sql = 'select name from v$database'
    result = cur.execute(sql)
    database_list = list(map(lambda x: x[0], result))   #得到的database_list是一个元组，list得到每个元组的第1个值，转换成列表
    return database_list

def get_database_name(tips,database_list):
    print(tips)
    for i in range(len(database_list)):
        print(str(i + 1) + ':' + database_list[i], end='\t')
    database_name = database_list[int(input('\n')) - 1]
    return database_name
    pass

def get_table_list(cur):
    sql = 'select table_name from user_tables'
    result = cur.execute(sql)
    table_list = list(map(lambda x: x[0], result))
    for i in range(len(table_list)):
        print('['+str(i + 1)+']'+table_list[i],end='\n')
    table_name = table_list[int(input('\n')) - 1]
    return table_name

def copy_table_struct(Source_table_name,Dst_table_name):
    sql_get_column_name = 'select COLUMN_NAME,DATA_TYPE,DATA_LENGTH from user_tab_columns where Table_name=\'%s\'' % Source_table_name
    Source_cur.execute(sql_get_column_name)
    Source_column_name = Source_cur.fetchall()
    #print(Source_column_name)

    sql_create_tabel = 'create TABLE %s(\n' % Dst_table_name
    for i in range(len(Source_column_name)-1):
        sql_create_tabel = sql_create_tabel + '%s %s(%d),\n' % (Source_column_name[i][0],Source_column_name[i][1],Source_column_name[i][2])
    sql_create_tabel = sql_create_tabel + '%s %s(%d) \n' % (Source_column_name[-1][0],Source_column_name[-1][1],Source_column_name[-1][2])
    sql_create_tabel = sql_create_tabel + ')'
    #这里拼凑create table 的语句

    #print(sql_create_tabel)
    Dst_cur.execute(str(sql_create_tabel))  #在目的数据库中执行


def copy_table_data(Source_table_name,Dst_table_name,):
    sql_get_column_name = 'select COLUMN_NAME from user_tab_columns where Table_name=\'%s\'' % Source_table_name
    Source_cur.execute(sql_get_column_name)
    Source_column_name = Source_cur.fetchall()
    sql_copy_data_p1 = 'INSERT INTO %s(' % Dst_table_name
    for i in range(len(Source_column_name)-1):
        sql_copy_data_p1 = sql_copy_data_p1 + '%s,' % Source_column_name[i]
    sql_copy_data_p1 = sql_copy_data_p1 + '%s)' % Source_column_name[-1]
    #print(sql_copy_data_p1)

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
        print(sql_copy_data_p2)
        Dst_cur.execute(str(sql_copy_data_p2))
        #time.sleep(0.5)
    Dst_conn.commit()

def run():
    try:
        connect_database()
        Source_database_list = get_database_list(Source_cur)
        Source_database_name = get_database_name('请输入来源数据库(输入序号):',Source_database_list)
        Dst_database_list = get_database_list(Dst_cur)
        Dst_database_name = get_database_name('请输入目标数据库(输入序号):',Dst_database_list)
        #print(Source_database_name)
        #print(Dst_database_name)
        Source_table_name = get_table_list(Source_cur)
        print(Source_table_name)
        Dst_table_name = str(input('请输入新的表名:\t'))
        print(Dst_table_name)
        copy_table_struct(Source_table_name,Dst_table_name)
        copy_table_data(Source_table_name,Dst_table_name)
        print('DATABASE TRANSFER SUCCESSFUL')
    finally:
        Source_conn.close()
        Dst_conn.close()
run()
