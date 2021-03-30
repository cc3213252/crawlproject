## 管理多个项目配置

https://docs.scrapy.org/en/latest/topics/commands.html

```bash
export SCRAPY_PROJECT=project2
scrapy settings --get BOT_NAME
```

## 建工程

```bash
scrapy startproject myproject [project_dir]
cd project_dir
scrapy genspider mydomain mydomain.com
```

## 调试

查看scrapy真正看到的内容
```bash
scrapy view https://www.cnvd.org.cn/flaw/list.htm
```

查看爬了哪些链接
```bash
scrapy parse http://quotes.toscrape.com/ --spider=toscrape-better 
```