#coding=utf-8
__author__ = 'xuxin'
import MySQLdb
def Connect():
    global conn
    conn = MySQLdb.connect(host='192.168.1.155',user='root',passwd='12345678',port=3307)
    conn.select_db('ssoc')

def testMysql():

    # cur = conn.cursor()
    query = 'select * from app_business'
    # count = cur.execute('select * from app_business')  #获取记录条数
    # result = cur.fetchall()
    conn.query(query)
    result = conn.use_result()
    if result:
        result = result.fetch_row(0,1)
    # cur.close()
    # print count
    print result

def testMysql2():
    cur = conn.cursor()
    query = 'select * from app_business'
    count = cur.execute(query)  #获取记录条数
    result = cur.fetchall()
    cur.close()
    print result


if __name__ == '__main__':
    Connect()
    testMysql()
    testMysql2()
    conn.close()
