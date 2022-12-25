import pymysql

class mysql_config:
    def __init__(self):
        self.host='XXXXXXXXXX'
        self.port=3306
        self.user="XXXXXXXXXX"
        self.passwd='XXXXXXXXXX'
        self.db='XXXXXXXXXX'
        self.conn=pymysql.connect(host=self.host,port=self.port,passwd=self.passwd,db=self.db,user=self.user)
        self.cursor=self.conn.cursor()


    #查询
    def sql_fetch(self,sql):
        self.cursor.execute(sql)
        results=self.cursor.fetchall()
        return results

    # 执行sql(创建、修改、删除)
    def sql_commit(self, sql, param=None):
        try:
            # 执行sql语句
            self.cursor.execute(sql, param)
            # 提交到数据库执行
            self.conn.commit()
        except Exception as e:
            print(e)
            # 如果发生错误则回滚
            self.conn.rollback()
            return False

        return True


    #关闭连接
    def close_db(self):
        self.cursor.close()
        self.conn.close()