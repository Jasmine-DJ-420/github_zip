#-*-coding:utf-8-*-
__author__ = 'DJ'

from scrapy.spiders import BaseSpider
from github_zip.items import GithubZipItem
import json
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
import requests
from lxml import html
from scrapy import Selector

page_count = -1

class ZipSpider(BaseSpider):

    access_token = "access_token=412ac4e93b48227b32c6f36d85276361e8b03f00"
    name = "zip"
    allowed_domains = ["github.com"]
    start_urls = [
        # "https://api.github.com/repositories?"+access_token +"&since=14842"
        # "https://github.com/pubnub/java",
        # "https://github.com/Donnervoegel/java",
        # "https://github.com/spinfo/java",
        # "https://github.com/douglascrockford/JSON-java",
        # "https://github.com/ReactiveX/RxJava",
        # "https://github.com/levelp/java",
        # "https://github.com/utnfrrojava/java",
        # "https://github.com/bborbe/java",
        # "https://github.com/iluwatar/java-design-patterns",
        # "https://github.com/Nirman-Rathod/Java",
        # "https://github.com/realm/realm-java",
        # "https://github.com/Mann02/java",
        # "https://github.com/javaee-samples/javaee7-samples",
        "https://github.com/hamcrest/JavaHamcrest",
        # "https://github.com/bcgit/bc-java",
        # "https://github.com/matyb/java-koans",
        # "https://github.com/aws/aws-sdk-java",
        # "https://github.com/apache/flex-sdk"
        # "https://github.com/apache/couchdb"
        # "https://github.com/apache/cordova-android"
        # "https://github.com/apache/harmony"
        # "https://github.com/apache/hadoop"
        # "https://github.com/apache/geronimo"
        # "https://github.com/apache/cassandra"
        # "https://github.com/apache/lucene-solr"
        # "https://github.com/apache/maven"
    ]
    download_warnsize = 0
    download_timeout = 1800

    def parse(self, response):
        global page_count
        page_count += 1

        url_domain = "https://github.com/"
        json_response = json.loads(response.body_as_unicode())

        header = response.headers
        link1 = header["Link"]
        link2 = link1.split("<")
        link = link2[1].split(">")[0]



        new_request = Request(link, callback=self.parse)
        yield new_request

        for full_names in json_response:
            item = GithubZipItem()
            full_name = full_names["full_name"].encode("utf-8")
            item['url'] = url_domain + full_name
            item['project_name'] = full_name.split('/')[1]
            item['user_name'] = full_name.split('/')[0]
            item['url_zip'] = item['url'] + "/archive/master.zip"
            request = Request(item['url'], callback=self.parse_java)
            request.meta['item'] = item
            yield request


        # 测试指定页面
        item = GithubZipItem()
        item['url'] = response.url
        item['project_name'] = item['url'].split('/')[-1]
        item['user_name'] = item['url'].split('/')[-2]
        # item['url_zip'] = item['url'] + "/archive/master.zip"
        request = Request(item['url'], callback=self.parse_java)
        request.meta['item'] = item
        yield request


    # whether it's a java project
    def parse_java(self,response):
        item = response.meta['item']
        sel = Selector(response)
        languages = sel.xpath("//span[@class='language-color']")
        for language in languages:
            java_flag = ('Java'==language.xpath("text()")[0].extract().encode("utf-8"))
            if java_flag:
                branch = sel.xpath("//div[@class='select-menu js-menu-container js-select-menu left']/button/span/text()")[0].extract().encode("utf-8")
                item['url_zip'] = item['url'] + "/archive/" + branch + ".zip"
                yield item








