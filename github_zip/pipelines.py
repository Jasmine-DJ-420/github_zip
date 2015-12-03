# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import os
import zipfile
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class MyFilePipeline(FilesPipeline):

    def __init__(self,store_uri,download_func = None):
        super(MyFilePipeline,self).__init__(store_uri=store_uri,download_func=download_func)
        self.zipfile_dj = store_uri
        self.store = self._get_store(store_uri)
        self.item_download = {}


    @classmethod
    def from_settings(cls, settings):
        store_uri = settings['ZIP_STORE']
        return cls(store_uri)

    def get_media_requests(self, item, info):
        yield Request(item["url_zip"],meta={'item': item})

    def item_completed(self, results, item, info):
        zip_files = [(x['path']) for ok, x in results if ok]
        if not zip_files:
            raise DropItem("Item contains no images")
        project = str(item["project_name"])
        user = str(item["user_name"])

        path = os.path.join(self.zipfile_dj,user+"_"+project)
        # 解压
        f = zipfile.ZipFile(os.path.join(self.zipfile_dj, zip_files[0]),"r")
        for file in f.namelist():
            f.extract(file,path)
        f.close()
        os.remove(os.path.join(self.zipfile_dj, zip_files[0]))

        self.del_files(path)

        # details.txt
        f = open(os.path.join(path,"details.txt"),"wb")
        f.write("project_name: "+item["project_name"]+"\n")
        f.write("user_name: "+item["user_name"]+"\n")
        f.write("url: "+item["url"])

        return item


    # delete non-java files
    def del_files(self, path):
        for root , dirs, files in os.walk(path):
            for name in files:
                if not name.endswith(".java"):
                    os.remove(os.path.join(root, name))

        for root,dirs,files in os.walk(path):
             if dirs == [] and files ==[]:
                 os.removedirs(root)