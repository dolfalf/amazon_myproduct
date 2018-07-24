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
        'https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Dfashion&field-keywords=%E5%B8%BD%E5%AD%90+%E3%83%AC%E3%83%87%E3%82%A3%E3%83%BC%E3%82%B9&rh=n%3A2229202051%2Ck%3A%E5%B8%BD%E5%AD%90+%E3%83%AC%E3%83%87%E3%82%A3%E3%83%BC%E3%82%B9',
    )

    # custom_settings = {'ROBOTSTXT_OBEY': False}

    def parse(self, response):

        for sel in response.xpath('//div[@class="s-item-container"]'):

            #タイトルに含まれている文字列を指定
            title_str = sel.xpath('div[@class="a-row a-spacing-none"]/div[@class="a-row a-spacing-mini"]/a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@title).extract_first()

            if 'UNICONA' in title_str:

                now = dt.now(timezone('Asia/Tokyo'))
                date = now.strftime('%Y-%m-%d')
                jst_time = now.strftime('%Y-%m-%dT%H-%M-%S')

                product = MyproductsItem()

                #タイトル
                sel.xpath('div[@class="a-row a-spacing-none"]/div[@class="a-row a-spacing-mini"]/a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@title).extract_first()
                #サームネイル
                product['thumbnail'] = sel.xpath('div[@class="a-row a-spacing-base"]/div/a/img/@src').extract_first()
                #キーワード
                product['keyword'] = response.xpath('//input[@id="twotabsearchtextbox"]/@value').extract_first()
                #リンク
                product['detail_link'] = sel.xpath('div[@class="a-row a-spacing-none"]/div[@class="a-row a-spacing-mini"]/div[position()=1]/a/@href').extract_first()
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
