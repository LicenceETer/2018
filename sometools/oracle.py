# -*- coding = utf-8 -*-
import cx_Oracle as cx

connect_info = {
    'user': 'c##test01',
    'password': 'test01',
    }
"""
conn = cx.connect(**connect_info)
print(conn.version)
cur = conn.cursor()
result = cur.fetchall()
print(result)
"""
"""
def get_table_stuc():
    sql = 'select COLUMN_NAME,DATA_TYPE,DATA_LENGTH from user_tab_cols where Table_Name='PERSONS';'
"""

def get_database_list():
    conn = cx.connect(**connect_info)
    cur = conn.cursor()
    sql = 'select name from v$database'
    result = cur.execute(sql)
    database_list = list(map(lambda x: x[0], result))
    conn.close()
    return database_list


def get_table_list(database):
    #connect_info.update({'database': database})
    conn = cx.connect(**connect_info)
    cur = conn.cursor()
    sql = 'select table_name from user_tables'
    result = cur.execute(sql)
    table_list = list(map(lambda x: x[0], result))
    print(table_list)
    conn.close()
    return table_list


def copy_table_struct(fromdatabase, todatabase, table_name):
    connect_info.update({'database': fromdatabase})
    from_conn = cx.connect(**connect_info)
    from_cur = from_conn.cursor()
    connect_info.update({'database': todatabase})
    to_conn = cx.connect(**connect_info)
    to_cur = to_conn.cursor()
    sql = 'show create table %s' % table_name
    create_sql = from_cur.execute(sql)[0][1]
    to_cur.execute(create_sql)
    to_conn.commit()
    to_conn.close()
    from_conn.close()


def copy_table_data(fromdatabase, todatabase, table_name):
    connect_info.update({'database': fromdatabase})
    from_conn = cx.connect(**connect_info)
    from_cur = from_conn.cursor()
    connect_info.update({'database': todatabase})
    to_conn = cx.connect(**connect_info)
    to_cur = to_conn.cursor()
    sql = 'select * from %s' % table_name
    result = from_cur.execute(sql)
    result = tuple([[str(x) for x in y] for y in result])
    for data in result:
        length = len(data)
        sql1 = 'insert into %s VALUES(' % table_name
        sql2 = '"%s",' * length % tuple(data)
        sql = sql1 + sql2[:-1] + ')'
        to_cur.execute(sql)
    to_conn.commit()
    to_conn.close()
    from_conn.close()


def run():
    database_list = get_database_list()
    print('请输入来源数据库(输入序号):')
    for i in range(len(database_list)):
        print(str(i + 1) + ':' + database_list[i], end='\t')
    from_database = database_list[int(input('\n')) - 1]
    print('请输入目标数据库(输入序号):')
    for i in range(len(database_list)):
        print(str(i + 1) + ':' + database_list[i], end='\t')
    to_database = database_list[int(input('\n')) - 1]
    print(from_database, to_database)
    table_list = get_table_list(from_database)
    for table in table_list:
        print('正在复制%s的结构...' % table)
        copy_table_struct(from_database, to_database, table)
        print('成功！')
        print('正在复制%s的数据...' % table)
        copy_table_data(from_database, to_database, table)
        print('成功！')
    print('任务结束！')


run()
