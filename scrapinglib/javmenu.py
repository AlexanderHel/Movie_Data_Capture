# -*- coding: utf-8 -*-

import re
from lxml import etree
from urllib.parse import urljoin

from .parser import Parser


class Javmenu(Parser):
    source = 'javmenu'

    expr_title = '/html/head/meta[@property="og:title"]/@content'
    expr_cover = '/html/head/meta[@property="og:image"]/@content'

    expr_number = '//span[contains(text(),"番號") or contains(text(),"Code")]/../a/text()'
    expr_number2 = '//span[contains(text(),"番號") or contains(text(),"Code")]/../span[2]/text()'
    expr_runtime = '//span[contains(text(),"時長;") or contains(text(),"Duration")]/../span[2]/text()'
    expr_release = '//span[contains(text(),"Publish Date")]/../span[2]/text()'
    expr_studio = '//span[contains(text(),"Publshier")]/../span[2]/a/text()'

    expr_actor = '//a[contains(@class,"actress")]/text()'
    expr_tags = '//a[contains(@class,"genre")]/text()'

    def extraInit(self):
        self.imagecut = 4
        self.uncensored = True

    def search(self, number):
        self.number = number
        if self.specifiedUrl:
            self.detailurl = self.specifiedUrl
        else:
            self.detailurl = 'https://javmenu.com/en/' + self.number + '/'
        self.htmlcode = self.getHtml(self.detailurl)
        if self.htmlcode == 404:
            return 404
        htmltree = etree.HTML(self.htmlcode)
        result = self.dictformat(htmltree)
        return result

    def getNum(self, htmltree):
        # 番号被分割开，需要合并后才是完整番号
        part1 = self.getTreeElement(htmltree, self.expr_number)
        part2 = self.getTreeElement(htmltree, self.expr_number2)
        dp_number =  part1 + part2
        # NOTE 检测匹配与更新 self.number
        if dp_number.upper() != self.number.upper():
            raise Exception(f'[!] {self.number}: find [{dp_number}] in javmenu, not match')
        self.number = dp_number
        return self.number

    def getTitle(self, htmltree):
        browser_title = super().getTitle(htmltree)
        # 删除番号
        number = re.findall("\d+",self.number)[1]
        title = browser_title.split(number,1)[-1]
        title = title.replace(' | JAV Menu | Update Daily',"")
        title = title.replace(' | JAV Menu | Update Daily',"").strip()
        return title.replace(self.number, '').strip()
    
