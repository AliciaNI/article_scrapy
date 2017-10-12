# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse  # python3 python2 导入的包为import urlparse

from article_scrapy.items import JobboleArticleItem

class JpbboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['www.jobbole.com']
    start_urls = ['http://python.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        1:从当前的url中获取文章列表的url并将他交给scrapy下载后并进行解析
        2：获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        :param response:
        :return:
        '''
        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            image_src = post_node.css('img::attr(src)').extract_first()
            post_url = post_node.css('::attr(href)').extract_first()
            yield Request(url=parse.urljoin(response.url, post_url),
                          dont_filter=True,
                          meta={'front_image_url':image_src},
                          callback=self.parse_detail)

       # 提取下一页并将其提交给scrapy下载
        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        '''
        # xpath获取文章内容
        # 提取标题 'Python 爬虫 (五) --多线程续 (Queue )'
        title = response.xpath('//*[@id="post-88413"]/div[1]/h1/text() ').extract_first('none')
        title2 = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('none')
        # 发布时间
        time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()')
        time = time.extract()[0].strip().split(" ")[0]
        # 赞的个数
        good_num = int(
            response.xpath(' // *[ @ id = "post-88413"] / div[3] / div[8] / span[1]/h10/text()').extract()[0])
        # 赞
        good = response.xpath(' // *[ @ id = "post-88413"] / div[3] / div[8] / span[1]/text()').extract()[1]
        # 收藏个数
        favorite = response.xpath('//*[@id="post-88413"]/div[3]/div[8]/span[2]/text()').extract()[0]
        favorite_num = int(re.match('.*(\d+).*', favorite).group(1))
        # 评论个数
        comment = response.xpath('//*[@id="post-88413"]/div[3]/div[8]/a/span/text()').extract()[0]
        comment_num = int(re.match('.*(\d+).*', comment).group(1))
        # 正文
        content = response.xpath('//div[@class="post-88413 post type-post status-publish format-standard '
                                 'hentry category-guide tag-1090 tag-714 odd"]/text()')
        content_id = response.xpath('//*[@id="post-88413"]/text()')
        content_whole = response.xpath('//div[@class="entry"]/text()')
        # ['系列教程', ' 3 评论 ', '多线程', '爬虫']
        content_head = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # ['系列教程', '多线程', '爬虫']
        content_filter = [element for element in content_head if not element.strip().endswith("评论")]
        content_filter = ','.join(content_filter)
        '''
        article_time = JobboleArticleItem()
        # css样式获取文章内容
        # 获取标题内容 Python 爬虫 (五) --多线程续 (Queue )
        title_css = response.css(".entry-header h1 ::text").extract()[0]
        # 异常处理  Python 爬虫 (五) --多线程续 (Queue )  如果第一个为空则返回设置的默认值none
        title_css_exception = response.css(".entry-header h1 ::text").extract_first('None')
        # 获取发布时间
        time = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip()
        time_css = time.replace(time[-1], "").strip()
        # 获取赞的个数
        good_num_css = int(response.css('.vote-post-up h10 ::text').extract()[0])
        # 收藏个数  2
        favorite = response.css('.bookmark-btn::text').extract()[0]
        favorite_num_css = re.match('.*(\d+).*', favorite)
        if favorite_num_css:
            favorite_num_css = int(favorite_num_css.group(1))
        else:
            favorite_num_css=0
        # 评论个数
        comment = response.css('.hide-on-480::text').extract()[2]
        # 方法2 利用a标签下的span获取span的文本内容
        comment2_css = response.css("a[href='#article-comment'] span::text").extract()[0]
        comment_num_css = re.match('.*(\d+).*', comment)
        if comment_num_css:
            num_css = int(comment_num_css.group(1))
        else:
            num_css = 0
        # 获取文章内容
        content_css = response.css('div.entry').extract()[0]
        # 头部信息
        content_head = response.css('p.entry-meta-hide-on-mobile a ::text').extract()
        content_list = [element for element in content_head if not element.strip().endswith("评论")]
        content_filter_css = ','.join(content_list)
        #获取图片url
        front_image_url = response.meta.get('front_image_url','none')

        article_time['title_css_exception']=title_css_exception
        article_time['time_css']=time_css
        article_time['url']=response.url
        article_time['front_image_url'] = {front_image_url}
        article_time['good_num_css'] = good_num_css
        article_time['favorite_num_css'] = favorite_num_css
        article_time['comment_num_css'] = comment_num_css
        article_time['content_filter_css'] = content_filter_css
        article_time['content_css'] = content_css

        yield article_time