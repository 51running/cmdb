from django.db import models
from django.db import connection

class AccessLogFile(models.Model):
    name = models.CharField(max_length=128,null=False,default='')
    path = models.CharField(max_length=1024,null=False,default='')
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)

class Accesslog(models.Model):
    file_id = models.IntegerField(default=0)
    ip = models.GenericIPAddressField(null=0,default='0.0.0.0')
    url = models.CharField(max_length=1024,null=False,default='')
    status_code = models.IntegerField(default=0,null=False)
    access_time = models.DateTimeField(null=False)

    @classmethod
    def dist_status_code(cls,file_id):
        cursor = connection.cursor()    #直接创建连接，获取游标
        cursor.execute("select status_code,count(*) from webanalysis_accesslog where file_id=%s group by status_code",(file_id))
        rt = cursor.fetchall()
        legend = []
        series = []
        for line in rt:
            legend.append(str(line[0]))
            # series.append({"name":line[0],"value":line[1]})    #line[0]为status_code，line[1]为count(*)，即次数
            series.append({"name":str(line[0]),"value":line[1]})    #line[0]为status_code，line[1]为count(*)，即次数
        return legend, series
    @classmethod
    def trend_visit(cls,file_id):
        cursor = connection.cursor()
        cursor.execute("select date_format(access_time, '%%Y-%%m-%%d %%H:00:00') as day, count(*) from webanalysis_accesslog where file_id=%s and access_time >= %s group by day;",(file_id,"1900.01.01"))
        rt = cursor.fetchall()
        xAxis = []
        series = []
        for line in rt:
            xAxis.append(line[0])
            series.append(line[1])

        return xAxis,series
