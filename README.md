## 纯文字静态网站爬取  
#### Lesson1 单页爬取
- scrapy startproject crawlproject
- scrapy genspider -t basic toscrape-xpath quotes.toscrape.com
- scrapy crawl toscrape-xpath -o toscrape-xpath.json
#### Lesson2 多页爬取1
#### Lesson3 多页爬取2
#### Lesson4 item使用
#### Lesson5 pipline使用
#### Lesson7 存储mongodb
- scrapy crawl toscrape-xpath

#### Lesson8 反爬之请求头限制


## 测试爬虫

- 修改setting中IMAGES_STORE目录
- 修改setting中ITEM_PIPELINES
