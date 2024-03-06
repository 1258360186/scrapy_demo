from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from demo.spiders.example import ExampleSpider
def run():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ExampleSpider)
    process.start()

if __name__ == '__main__':
    run()