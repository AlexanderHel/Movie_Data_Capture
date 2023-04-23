# -*- coding: utf-8 -*-

import re
from lxml import etree

from .parser import Parser


class Javct(Parser):
    source = 'javct'

    expr_title = '/html/head/title/text()'
    expr_cover = '//img[@class="cover"]/@src'
    expr_label = '//li[contains(span, "Label")]/text()'
    expr_runtime = '//li[contains(span, "Running time")]/text()'
    expr_release = '//li[contains(span, "Release Date")]/text()'
    expr_studio = '//li[contains(span, "Studio")]//strong/text()'
    expr_actor = '//li[contains(span, "Model")]/a/strong/text()'
    expr_actorphoto = '//div[@class="card__cover"]/img/@src'
    expr_tags = '//li[contains(span, "Categories")]/a/strong/text()'

    def extraInit(self):
        self.uncensored = True

    def search(self, number):
        self.number = number
        if self.specifiedUrl:
            self.detailurl = self.specifiedUrl
        else:
            self.detailurl = 'https://javct.net/v/' + self.number
        self.htmlcode = self.getHtml(self.detailurl)
        if self.htmlcode == 404:
            return 404
        htmltree = etree.HTML(self.htmlcode)
        result = self.dictformat(htmltree)
        return result

    def getNum(self, htmltree):
        return self.number
    
