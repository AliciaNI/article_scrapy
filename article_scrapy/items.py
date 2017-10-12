# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobboleArticleItem(scrapy.Item):
    title_css_exception =scrapy.Field()
    time_css =scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    good_num_css = scrapy.Field()
    favorite_num_css = scrapy.Field()
    comment_num_css = scrapy.Field()
    content_filter_css = scrapy.Field()
    content_css = scrapy.Field()



