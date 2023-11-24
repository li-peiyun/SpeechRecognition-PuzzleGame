class dbUtils:
    def __init__(self, dbName):  # 连接数据库
        import sqlite3
        self.conn = sqlite3.connect(dbName)

    def db_action(self, sql, actionType=0):  # 进行相关业务操作
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)

            if actionType == 1:  # 当操作类型为1时代表为查询业务，返回查询列表
                columns = [col[0] for col in cursor.description]
                results = cursor.fetchall()

                # 将结果转换为字典列表
                result_dicts = [dict(zip(columns, row)) for row in results]
                return result_dicts
            else:  # 当操作类型不为1时代表为新增、删除或更新业务，返回逻辑值
                return True
        except ValueError as e:
            print(e)

    def close(self):  # 关闭数据库
        self.conn.commit()
        self.conn.close()

