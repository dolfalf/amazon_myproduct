# amazon_myproduct

- デバックコマンド

`scrapy shell  "https://www.amazon.co.jp/s/ref=sr_pg_2/357-7434527-9428017?rh=i%3Aaps%2Ck%3A%E5%B8%BD%E5%AD%90+%E3%83%AC%E3%83%87%E3%82%A3%E3%83%BC%E3%82%B9&page=2&keywords=%E5%B8%BD%E5%AD%90+%E3%83%AC%E3%83%87%E3%82%A3%E3%83%BC%E3%82%B9&ie=UTF8&qid=1532240763"`

実行できからこんな感じでreponseから確認できる

`response.xpath('//input[@id="twotabsearchtextbox"]@value').extract()[0]`

デバック中止は `Ctrl+D`

- クローラー実行＆ファイル出力

`scrapy crawl searchProducts -o sample_data.csv`

- scrapyをクラウドでできる

https://scrapinghub.com/


## 参考サイト

- scrapy+scrapinghub

https://data.gunosy.io/entry/python-scrapy-scraping
