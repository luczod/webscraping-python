from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article


# scrapy runspider articleItems.py
# scrapy runspider articleItems.py articles -O articles.json:json
class ArticleSpider(CrawlSpider):
    name = 'articleItems'
    allowed_domains = ['wikipedia.org']
    start_urls = [
        'https://en.wikipedia.org/wiki/'
        'Benevolent_dictator_for_life'
    ]
    rules = [
        Rule(LinkExtractor(allow=r'.*'), callback='parse_items', follow=True)
    ]

    def parse_items(self, response):
        article = Article()
        article['url'] = response.url
        article['title'] = response.css('h1::text').extract_first()
        article['text'] = response.xpath(
            '//div[@id="mw-content-text"]//text()').extract()

        lastUpdated = response.css(
            'li#footer-info-lastmod::text').extract_first()
        lastUpdated = lastUpdated.replace('This page was last edited on ', '')

        print('URL is: {}'.format(article['url']))
        print('title is: {} '.format(article['title']))
        print('text is: {}'.format(article['text']))
        print('Last updated: {}'.format(lastUpdated))
