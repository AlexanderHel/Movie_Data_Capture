import sys
sys.path.append('../')

from WebCrawler.crawler import *
from ADC_function import *
from lxml import etree

def main(number):
    try:
        number = number.upper().replace('GCOLLE-','')
        session = get_html_session()

        htmlcode = session.get('https://gcolle.net/product_info.php/products_id/' + number).text
        html = etree.HTML(htmlcode)
        # R18 countinue
        htmlcode = session.get(html.xpath('//*[@id="main_content"]/table[1]/tbody/tr/td[2]/table/tbody/tr/td/h4/a[2]/@href')[0]).text
        gcolle_crawler = Crawler(htmlcode)

        number_html = gcolle_crawler.getString('//td[contains(text(),"商品番号")]/../td[2]/text()')
        if number != number_html:
            raise Exception('[-]gcolle.py: number not match')

        # get extrafanart url
        if len(gcolle_crawler.getStrings('//*[@id="cart_quantity"]/table/tr[3]/td/div/img/@src')) == 0:
            extrafanart = gcolle_crawler.getStrings('//*[@id="cart_quantity"]/table/tr[3]/td/div/a/img/@src')
        else:
            extrafanart = gcolle_crawler.getStrings('//*[@id="cart_quantity"]/table/tr[3]/td/div/img/@src')
        # Add "https:" in each extrafanart url
        for i in range(len(extrafanart)):
            extrafanart[i] = 'https:' + extrafanart[i]

        dic = {
            "title":      gcolle_crawler.getString('//*[@id="cart_quantity"]/table/tr[1]/td/h1/text()'),
            "studio":     gcolle_crawler.getString('//td[contains(text(),"アップロード会員名")]/b/text()'),
            "year":       re.findall('\d{4}',gcolle_crawler.getString('//td[contains(text(),"商品登録日")]/../td[2]/time/@datetime'))[0],
            "outline":    gcolle_crawler.getOutline('//*[@id="cart_quantity"]/table/tr[3]/td/p/text()'),
            "runtime":    '',
            "director":   gcolle_crawler.getString('//td[contains(text(),"アップロード会員名")]/b/text()'),
            "actor":      gcolle_crawler.getString('//td[contains(text(),"アップロード会員名")]/b/text()'),
            "release":    re.findall('\d{4}-\d{2}-\d{2}',gcolle_crawler.getString('//td[contains(text(),"商品登録日")]/../td[2]/time/@datetime'))[0],
            "number":     "GCOLLE-" + str(number_html),
            "cover":      "https:" + gcolle_crawler.getString('//*[@id="cart_quantity"]/table/tr[3]/td/table/tr/td/a/@href'),
            "thumb":      "https:" + gcolle_crawler.getString('//*[@id="cart_quantity"]/table/tr[3]/td/table/tr/td/a/@href'),
            "trailer":    '',
            "actor_photo":'',
            "imagecut":   4, # 该值为4时同时也是有码影片 也用人脸识别裁剪封面
            "tag":        gcolle_crawler.getStrings('//*[@id="cart_quantity"]/table/tr[4]/td/a/text()'),
            "extrafanart":extrafanart,
            "label":      gcolle_crawler.getString('//td[contains(text(),"アップロード会員名")]/b/text()'),
            "website":    'https://gcolle.net/product_info.php/products_id/' + number,
            "source":     'gcolle.py',
            "series":     gcolle_crawler.getString('//td[contains(text(),"アップロード会員名")]/b/text()'),
            '无码': False,
        }
        # for k,v in dic.items():
        #     if k == 'outline':
        #         print(k,len(v))
        #     else:
        #         print(k,v)
        # print('===============================================================')
    except Exception as e:
        dic = {'title':''}
        if config.getInstance().debug():
            print(e)

    return dic

if __name__ == '__main__':
    from pprint import pprint
    config.getInstance().set_override("debug_mode:switch=1")
    pprint(main('840724'))
    pprint(main('840386'))
    pprint(main('838671'))
    pprint(main('814179'))
    pprint(main('834255'))
    pprint(main('814179'))
