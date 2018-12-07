#! *_* coding: utf-8 *_*

import scrapy
from lxml import etree
import re
from datetime import datetime
from scrapy.http import Request
from ..items import HexunItem, DataItem
from .. import loggers

class hexunSpider(scrapy.Spider):
    name = 'hexun'
    allowed_domains = ['quote.hexun.com', 'quote.tool.hexun.com']
    start_urls = ['http://quote.hexun.com/default.htm']

    def parse(self,response):
        html = etree.HTML(response.text.encode('utf-8').decode('utf-8'))
        ul = html.xpath('//div[@id="folder_Agsc"]/ul')
        lis = ul[0].xpath('./li')
        classify_name = lis[1].text.strip('\t|" "|\n')
        links = lis[1].xpath('.//@href')
        names = lis[1].xpath('.//a/text()')
        hexun_item = HexunItem()
        hexun_item['classify_name'] = classify_name
        hexun_item['links'] = ['http://quote.hexun.com/%s' %url for url in links]
        hexun_item['names'] = names
        yield hexun_item

        for c_n in range(len(names)):
            url = links[c_n]
            p = re.compile(r'\?code.*?&').search(url)
            if p:
                t_now = datetime.now()
                #gettime = datetime.strftime(t_now, '%H%M%S')
                gettime = '143030'
                code = 'type_' + p.group()[1:-1]
                url = 'http://quote.tool.hexun.com/hqzx/stocktype2.aspx?columnid=5517&'\
                      + code + '&sorttype=3&updown=up&page=1&count=50&' + gettime
                req = Request(url, callback=self.getdata)
                req.meta['classify_name'] = names[c_n]
                yield req

    def getdata(self, response):
        datas = DataItem()
        text = response.text
        a = text.split(';Stock')[0].strip('\n|" "')
        try:
            exec(a)
        except Exception, e:
            loggers.error('have a error:%s' % str(e))
            p = re.compile(r'[0-9].*[0-9]')
            b = p.search(a.split('=')[1]).group().split('],[')
            dataArr = []
            for one in b:
                l_s = [i.strip('\'|\"') for i in one.split(',')]
                l_s[9] = int(l_s[9])
                for n in [2,3,4,5,6,7,8,10,11,12]:
                    try:
                        l_s[n] = float(l_s[n])
                    except Exception,e:
                        l_s[n] = 0.00
                dataArr.append(l_s)
        if dataArr:
            datas['data'] = dataArr
            datas['classify_name'] = response.meta['classify_name']
            yield datas
            for i in range(2,10):
                if len(dataArr) == 50:
                    url = response.url
                    num = url.find('page=')
                    if num >= 0:
                        url = url.replace(url[num: num+6], 'page=%s' % str(i))
                        req = Request(url, callback=self.getdata)
                        req.meta['classify_name'] = datas['classify_name']
                        yield req
                    else:
                        loggers.error('error logical')
                else:
                    break
        else:
            loggers.info('samll probability ojbk')





        #a = text.split('=')[1].split(';Stock')[0][5:-1].split('],[')
        #print a
        # data = [one.split(',') for one in a]
        # for row in data:
        #     row[0] = row[0].strip('\'|\"')
        #     row[1] = row[1].strip('\'|\"')
        #     row[9] = int(row[9])
        #     for idx in [2,3,4,5,6,7,8,10,11,12]:
        #         self.tofloat(row, idx)
        # datas['data'] = data
        # yield datas
    #
    # def tofloat(self, row, idx):
    #     try:
    #         row[idx] = float(row[idx])
    #     except Exception, e:
    #         #row[idx] = 0
    #         loggers.info('some logical error:%s,%s' %(str(e), row[idx]))



