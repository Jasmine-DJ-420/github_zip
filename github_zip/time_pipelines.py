#-*-coding:utf-8-*-
__author__ = 'DJ'

from scrapy import signals
import os

class time_pipeline(object):

    def __init__(self, stats):
        self.stats = stats
        self.num_errors = 0
        self.errors = []

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.stats)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_closed(self, spider):
        start_time = self.stats._stats['start_time']
        finish_time = self.stats._stats['finish_time']
        os.removedirs("/usr/dj/Crawl_data/github/JAVA/full")
        print finish_time - start_time