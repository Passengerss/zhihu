# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request,Spider
import json
from ..items import *

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # 路人甲
    start_user_url_token = "sgai"

    # 个人详细信息url
    user_url = "https://www.zhihu.com/api/v4/members/{user_url_token}?include={include}"
    user_query = "allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics"
    # 他所关注的用户
    follows_url = "https://www.zhihu.com/api/v4/members/{user_url_token}/followees?include={include}&offset={offset}&limit={limit}"
    follows_query = "data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics"
    # 他的粉丝
    followers_url = "https://www.zhihu.com/api/v4/members/{user_url_token}/followers?include={include}&offset={offset}&limit={limit}"
    followers_query = "data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics"
    def start_requests(self):
        yield Request(url=self.user_url.format(user_url_token=self.start_user_url_token,include=self.user_query),callback=self.parse_user)
        yield Request(url=self.follows_url.format(user_url_token=self.start_user_url_token,include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
        yield Request(url=self.followers_url.format(user_url_token=self.start_user_url_token,include=self.followers_query,offset=0,limit=20),callback=self.parse_followers)

    # 处理一个用户
    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        # 递归每一个用户的关注列表
        yield Request(url=self.follows_url.format(user_url_token=result.get("url_token"),include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
        # 递归每一个用户的粉丝列表
        yield Request(url=self.followers_url.format(user_url_token=result.get("url_token"),include=self.followers_query,offset=0,limit=20),callback=self.parse_followers)

    # 处理关注列表
    def parse_follows(self,response):
        result = json.loads(response.text)
        # 是否含有数据且非最后一页
        if "data" in result.keys():
            for result in result.get("data"):
                yield Request(url=self.user_url.format(user_url_token=result.get("url_token"),include=self.user_query),callback=self.parse_user)

        if "paging" in result.keys() and result.get("paging").get("is_end") == False:
            next_page = result.get("paging").get("next")
            yield Request(url=next_page,callback=self.parse_follows)

    def parse_followers(self,response):
        result = json.loads(response.text)
        # 是否含有数据且非最后一页
        if "data" in result.keys():
            for result in result.get("data"):
                yield Request(url=self.user_url.format(user_url_token=result.get("url_token"),include=self.user_query),callback=self.parse_user)

        if "paging" in result.keys() and result.get("paging").get("is_end") == False:
            next_page = result.get("paging").get("next")
            yield Request(url=next_page,callback=self.parse_followers)