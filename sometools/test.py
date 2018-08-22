# -*- coding = utf-8 -*-
import cx_Oracle as cx

connect_info = {
    'user': 'c##test01',
    'password': 'test01',
    }

conn = cx.connect(**connect_info)
cur = conn.cursor()
sql = """CREATE TABLE python_modules (
        module_name VARCHAR2(50) NOT NULL,
        file_path VARCHAR2(300) NOT NULL
        )"""
sql= """INSERT INTO PERSONS(
        name,
        city,
        age,
        phone_number)
        VALUES(
        'pony',
        'shenzhen',
        '43',
        '12368576'
        );"""
sql1="INSERT INTO test3(NAME,CITY,AGE,PHONE_NUMBER)VALUES('jssff',Null,Null,Null)"
cur.execute(sql1)
#result = cur.fetchall()
#result = tuple([[str(x) for x in y] for y in result])

#conn.commit()
