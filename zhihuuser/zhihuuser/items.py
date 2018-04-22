# -*- coding: utf-8 -*-
from scrapy import Field,Item

class UserItem(Item):
    allow_message = Field()
    answer_count = Field()
    articles_count = Field()
    avatar_url = Field()
    badge = Field()
    employments = Field()
    company = Field()
    follower_count = Field()
    gender = Field()
    headline = Field()
    id = Field()
    is_advertiser = Field()
    is_blocking = Field()
    is_followed = Field()
    is_following = Field()
    is_org = Field()
    name = Field()
    type = Field()
    url = Field()
    url_token = Field()
    user_type = Field()