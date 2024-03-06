import time
from typing import Iterable
from urllib.parse import urlencode

import scrapy
from scrapy import Request


# 目录接口
# https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=43895466&pageNum=1&pageSize=30
# 音频接口
# https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/1709704217252?device=www2&trackId=356538909&trackQualityLevel=1
class XimalayaSpider(scrapy.Spider):
    name = "ximalaya"
    allowed_domains = ["www.ximalaya.com"]
    start_url = "https://www.ximalaya.com/tdk-web/seo/search/albumInfo"
    albumIds = [43895466]

    def __init__(self):
        super().__init__()
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

    def start_requests(self):
        for albumId in self.albumIds:
            params = {
                'albumId': albumId
            }

            proxy = {
                'http': 'http://127.0.0.1:7890',
                'https': 'http://127.0.0.1:7890',
            }

            url = f'{self.start_url}?{urlencode(params)}'

            yield Request(url,method='GET',headers=self.headers,meta={'albumId': albumId},callback=self.parse)




    def parse(self, response):
        albumId = response.meta['albumId']
        response = response.json()
        if response['ret'] != 200:
            raise ValueError('发生了一个错误')
        trackCount = response['data']['trackCount']
        pageNums = trackCount//30 + 1
        for pageNum in range(1, pageNums+1):
            params = {
                'albumId': albumId,
                'pageNum': pageNum,
                'pageSize': 30
            }
            url = f"https://www.ximalaya.com/revision/album/v1/getTracksList?{urlencode(params)}"
            yield Request(url, method='GET',headers=self.headers,callback=self.parse_detail)


    def parse_detail(self, response):
        # trackId = response.meta['albumId']
        # trackQualityLevel = response.meta['pageNum']
        response = response.json()
        if response['ret'] != 200:
            raise ValueError('发生了一个错误')
        tracks = response['data']['tracks']
        for track in tracks:
            trackId = track['trackId']
            # level = track['trackQualityLevel']
            params = {
                'device' : 'www2',
                'trackId': trackId,
                'trackQualityLevel': 1,
            }

            url = f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time())}?{urlencode(params)}"
            yield Request(url, callback=self.parse_sound, method='GET', headers=self.headers)

    def parse_sound(self, response):
        response = response.json()
        playUrlList = response['trackInfo']['playUrlList']
        MP3_64_url = playUrlList[1]['url']

        pass
