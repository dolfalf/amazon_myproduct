# -*- coding: utf-8 -*-
import scrapy
from pytz import timezone
from datetime import datetime as dt
from myproducts.items import MyproductsItem

class SearchproductsSpider(scrapy.Spider):
    name = 'searchProducts'
    allowed_domains = ['amazon.co.jp']

    #カテゴリリンクを追加します。
    start_urls = (
        # micro usb ケーブル
        'https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Delectronics&field-keywords=micro+usb+%E3%82%B1%E3%83%BC%E3%83%96%E3%83%AB&rh=n%3A3210981%2Ck%3Amicro+usb+%E3%82%B1%E3%83%BC%E3%83%96%E3%83%AB',
        # 小便器
        'https://www.amazon.co.jp/s/ref=sr_pg_1?rh=i:aps,k:%E5%B0%8F%E4%BE%BF%E5%99%A8&keywords=%E5%B0%8F%E4%BE%BF%E5%99%A8&ie=UTF8&qid=1529493127',
        # 帽子 レディース
        'https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords=%E5%B8%BD%E5%AD%90+%E3%83%AC%E3%83%87%E3%82%A3%E3%83%BC%E3%82%B9&rh=i%3Aaps%2Ck%3A%E5%B8%BD%E5%AD%90+%E3%83%AC%E3%83%87%E3%82%A3%E3%83%BC%E3%82%B9',
        # FBA 帽子 レディース つば広
        'https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Dfashion-womens-clothing&field-keywords=%E5%B8%BD%E5%AD%90+%E3%83%AC%E3%83%87%E3%82%A3%E3%83%BC%E3%82%B9+%E3%81%A4%E3%81%B0%E5%BA%83&rh=i%3Afashion-womens-clothing%2Ck%3A%E5%B8%BD%E5%AD%90+%E3%83%AC%E3%83%87%E3%82%A3%E3%83%BC%E3%82%B9+%E3%81%A4%E3%81%B0%E5%BA%83',

        ,
    )

    # custom_settings = {'ROBOTSTXT_OBEY': False}

    def parse(self, response):

        for sel in response.xpath('//div[@class="s-item-container"]'):

            #タイトルに含まれている文字列を指定
            title_str = sel.xpath('div[@class="a-row a-spacing-mini"]/div[position()=1]/a/@title').extract_first()
            if 'FEREX' in title_str \
                or 'TS.CORP' in title_str \
                or 'UNICONA' in title_str:

                now = dt.now(timezone('Asia/Tokyo'))
                date = now.strftime('%Y-%m-%d')
                jst_time = now.strftime('%Y-%m-%dT%H-%M-%S')
                
                product = MyproductsItem()

                #タイトル
                sel.xpath('div[@class="a-row a-spacing-mini"]/div[position()=1]/a/@title').extract_first()
                #サームネイル
                product['thumbnail'] = sel.xpath('div[@class="a-row a-spacing-base"]/div/div[position()=1]/a/img/@src').extract_first()
                #キーワード
                product['keyword'] = response.xpath('//span[@id="breadcrumbJSnonCompatible"]/span/text()').extract_first()
                #リンク
                product['detail_link'] = sel.xpath('div[@class="a-row a-spacing-mini"]/div[position()=1]/a/@href').extract_first()
                #ページカウント
                product['page_count'] = response.xpath('//div[@id="bottomBar"]/div/span[@class="pagnCur"]/text()').extract_first()
                #ページURL
                product['url'] = response.url
                #データ取得時刻
                product['timestamp'] = jst_time

                yield product

        next_page = response.xpath('//a[@id="pagnNextLink"]/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, callback=self.parse)
        # pass
