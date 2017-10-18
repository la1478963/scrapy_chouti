# -*- coding: utf-8 -*-
import scrapy
import sys
import io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
from scrapy.selector import Selector,HtmlXPathSelector
from scrapy.http import Request
from ..items import WormItem

class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['dig.chouti.com']
    start_urls = ['http://dig.chouti.com/']
    url_set=set()

    def parse(self, response):
        # content=str(response.body,encoding='utf-8')
        # print(content)
        # a_l=Selector(response=response).xpath('//a')#标签对象列表
        # a_l=Selector(response=response).xpath('//a').extract()#标签对象列表里面的标签对象变成字符串

        # JG1=Selector(response=response).xpath('//head')
        # JG=JG1.xpath('.//title/text()').extract()
        # print(JG)

        #拿到单页的所有标签
        item_list=Selector(response=response).xpath('//div[@id="content-list"]/div[@class="item"]')
        for item in item_list:
            title=item.xpath('.//a[@class="show-content color-chag"]/text()').extract_first().strip()
            chouti_url=item.xpath('.//a[@class="show-content color-chag"]/@href').extract_first().strip()
            # a_list=item.xpath('.*//a[@class="show-content"]/text()').extract_first()
            item_obj=WormItem(title=title,url=chouti_url)
            return item_obj


        #拿页码
        #拿本页的所有页码
        page_l=Selector(response=response).xpath('//div[@id="dig_lcpage"]//a/@href').extract()

        for page in page_l:
            page = 'http://dig.chouti.com' + page
            #判断是不是重复
            if page not in self.url_set:
                self.url_set.add(page)
                #回调，   知识点： 类属性只有在程序执行的时候会加载，所以  类属性 url_set 不会刷掉
                yield Request(url=page,callback=self.parse)
