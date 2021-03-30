## 资料

https://docs.scrapy.org/en/latest/intro/tutorial.html

## tutorial

```bash
scrapy crawl quotes -O quotes-humor.json -a tag=humor
```
给scrapy的__init__传递了一个参数tag，用于只爬取一部分