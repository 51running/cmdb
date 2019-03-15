#encoding:utf-8
import traceback
from django.db import connection


class MysqlConnect(object):

    @classmethod
    def excute_sql(cls,sql,args=(),fetch=True,one=False):
        cnt, result = 0 ,None
        cursor = None
        try:
            cursor = connection.cursor()
            cnt= cursor.execute(sql,args)
            if fetch:
                result = cursor.fetchone() if one else cursor.fetchall()
            else:
                connection.commit()
        except BaseException as e:
            print(e)
            print(traceback.format_exc())
        finally:
            if cursor:
                cursor.close()
        return cnt, result