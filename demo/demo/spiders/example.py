import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def __init__(self):
        super.__init__()
        self.headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        self.url = "https://example.com/"

    def start_requests(self):
        params={

        }

        data = {

        }

        proxy = {
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890',
        }

        yield scrapy.Request(self.url,method='GET' ,headers=self.headers, callback=self.parse,dont_filter=True,meta={'proxy': proxy})

    def parse(self, response):
        pass
