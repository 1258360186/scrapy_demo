from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from demo.spiders.ximalaya import XimalayaSpider
def run():
    process = CrawlerProcess(get_project_settings())
    process.crawl(XimalayaSpider)
    process.start()

if __name__ == '__main__':
    run()