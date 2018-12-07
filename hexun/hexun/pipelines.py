# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import pymysql.cursors
from hexun.items import HexunItem, DataItem
from hexun import settings
from . import loggers

class HexunPipeline(object):
    def __init__(self):
        self.con = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.con.cursor()
        self.con.autocommit(True)

    def process_item(self, item, spider):
        if isinstance(item, HexunItem):
            try:
                for n in range(len(item['links'])):
                    self.cursor.execute("select * from classify where url='%s'" %item['links'][n])
                    if self.cursor.fetchone():
                        pass
                    else:
                        self.cursor.execute("""
                            insert into classify(url, classify_name, industry) value ('%s','%s','%s')"""
                            %(item['links'][n], item['names'][n], item['classify_name']))
            except Exception, e:
                print e
            return item
        elif isinstance(item, DataItem):
            try:
               # for one in item['data']:
                    # print item['classify_name'], one[0], one[1] ,one[2], one[3], one[4],\
                    #       one[5], one[6], one[7], one[8], one[9], one[10], one[11], one[12]

                    # print '''insert into datas(classify_name, code, code_name, new_price, up_down, y_price, t_price,
                    #       highest, lowest, volumes, turnover, changed, amplitude, per) value (%s, %s, %s, %.2f, %.2f, %.2f,%.2f,
                    #       %.2f, %.2f, %.2f, %d, %.2f, %.2f, %.2f)''' %(item['classify_name'], one[0], one[1].decode('utf-8') ,one[2], one[3], one[4],
                    #       one[5], one[6], one[7], one[8], one[9], one[10], one[11], one[12])
                    #self.cursor.execute("""
                    #     insert into datas(classify_name, code, code_name, new_price, up_down, y_price, t_price,
                    #     highest, lowest, volumes, turnover, changed, amplitude, per) value ('%s', '%s', '%s', %.2f,
                    #     %.2f, %.2f,%.2f, %.2f, %.2f, %.2f, %d, %.2f, %.2f, %.2f)""" \
                    #     %(item['classify_name'], one[0], one[1].decode('utf-8') ,one[2], one[3], one[4], one[5], one[6], one[7],
                    #       one[8], one[9], one[10], one[11], one[12]))
            except Exception, e:
                loggers.error('%s' %e)





