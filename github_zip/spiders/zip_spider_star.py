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

page_count = 1

class ZipSpider(BaseSpider):

    name = "zip_star"
    allowed_domains = ["github.com"]
    start_urls = [
        "http://github-awards.com/users?language=Java&type=world&utf8=%E2%9C%93&page=6",
        "http://github-awards.com/users?language=Java&type=world&utf8=%E2%9C%93&page=7",
        "http://github-awards.com/users?language=Java&type=world&utf8=%E2%9C%93&page=8",
        "http://github-awards.com/users?language=Java&type=world&utf8=%E2%9C%93&page=9",
        "http://github-awards.com/users?language=Java&type=world&utf8=%E2%9C%93&page=10",
    ]
    download_warnsize = 0
    download_timeout = 1800

    def parse(self, response):
        global page_count

        sel = Selector(response)
        usernames = sel.xpath("//td[@class='username']/a")
        for username in usernames:
            user_name = username.xpath("text()")[0].extract().encode("utf-8")
            url = "https://github.com/" + user_name + "/repositories"
            request = Request(url, callback=self.parse_repositories)
            request.meta['user_name'] = user_name
            yield request

    # parse_repositories:
    def parse_repositories(self, response):
        user_name = response.meta['user_name']
        url_domain = "https://github.com/"
        sel = Selector(response)
        projects = sel.xpath("//li[@class='repo-list-item public source']")

        next_page = sel.xpath("//a[@class='next_page']/@href")
        if(next_page):
            link = next_page[0].extract().encode("utf-8")
            request = Request("https://github.com" + link, callback=self.parse_repositories)
            request.meta['user_name'] = user_name
            yield request


        for project in projects:
            language = project.xpath("div[@class='repo-list-stats']/text()")[0].extract().strip().encode("utf-8")
            if('Java'==language):
                item = GithubZipItem()
                item["user_name"] = user_name
                item["project_name"] = project.xpath('h3/a/text()')[0].extract().strip().encode("utf-8")
                item["url"] = url_domain + item["user_name"] + "/" + item["project_name"]
                request = Request(item['url'], callback=self.parse_java)
                request.meta['item'] = item
                yield request

    # whether it's a java project
    def parse_java(self,response):
        item = response.meta['item']
        sel = Selector(response)
        branch = sel.xpath("//div[@class='select-menu js-menu-container js-select-menu left']/button/span/text()")[0].extract().encode("utf-8")
        item['url_zip'] = item['url'] + "/archive/" + branch + ".zip"
        yield item








