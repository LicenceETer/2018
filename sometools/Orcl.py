#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cx_Oracle as cx

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
        Source_conn = cx.connect(**Source_databse_info)
    except:
        print('Connect to Source Databse Failed , Please Check Connection Info')
        os._exit(0)
    try:
        Dst_conn = cx.connect(**Dest_database_info)
    except :
        print('Connect to Destination Databse Failed , Please Check Connection Info')
        os._exit(0)
    global Source_cur
    Source_cur = Source_conn.cursor()
    global Dst_cur
    Dst_cur = Dst_conn.cursor()
    print('The Source Database version is '+ Source_conn.version )
    print('The Destination Database version is ' + Dst_conn.version)
    return Source_cur,Dst_cur
    pass

def get_database_list(cur):
    sql = 'select name from v$database'
    result = cur.execute(sql)
    database_list = list(map(lambda x: x[0], result))
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
    print(Source_column_name)
    sql_create_tabel = 'create table %s(' % Dst_table_name
    for i in range(len(Source_column_name)-1):
        sql_create_tabel = sql_create_tabel + '%s %s(%d),' % (Source_column_name[i][0],Source_column_name[i][1],Source_column_name[i][2])
    sql_create_tabel = sql_create_tabel + '%s %s(%d)' % (Source_column_name[-1][0],Source_column_name[-1][1],Source_column_name[-1][2])
    sql_create_tabel = sql_create_tabel + ');'
    print(sql_create_tabel)
    Dst_cur.execute(sql_create_tabel)
    print(Dst_cur.fetchall())
    
def run():
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
run()
