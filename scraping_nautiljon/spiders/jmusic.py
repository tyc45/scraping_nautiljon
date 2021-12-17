import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector.unified import Selector
from scrapy.spiders import CrawlSpider, Rule
from scraping_nautiljon.items import ScrapingNautiljonItem


class JmusicSpider(CrawlSpider):
    name = 'jmusic'
    allowed_domains = ['www.nautiljon.com']
    # user_agent allows the spider to be recognized as a browser
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'
    
    def start_requests(self):
        """This method uses the user_agent on the specified url to crawl as a browser

        Yields:
            [type]: [description]
        """        
        yield scrapy.Request(url='https://www.nautiljon.com/jmusic/?q=z&dbt=0', headers={
            'User-Agent': self.user_agent
    })

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//td/span[@class="fright"]/following-sibling::a'), 
            callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths='//p[@class="menupage"][1]/a[text()=">>"]'),
            follow=True, process_request='set_user_agent'),
    )

    def parse_item(self, response):
        item = ScrapingNautiljonItem()
        item["title"] = Selector(response).xpath('//h1/span[@itemprop="name"]/text()').get()
        item["type"] = Selector(response).xpath('//span[text()="Type : "]/following-sibling::text()').get()
        item["release_date"] = Selector(response).xpath('//span[@itemprop="datePublished"]/text()').get()
        item["label"] = Selector(response).xpath('//span[@itemprop="legalName"]/text()').get()
        item["producer"] = Selector(response).xpath('//span[text()="Distributeur : "]/following-sibling::a/text()').get()
        item["artists"] = Selector(response).xpath('//span[@itemprop="byArtist"]/text()').getall()
        item["lyrics"] = Selector(response).xpath('//span[text()="Paroles : "]/following-sibling::a/text()').getall()
        item["composers"] = Selector(response).xpath('//span[text()="Compositeurs : "]/following-sibling::a/text()').getall()
        item["arrangers"] = Selector(response).xpath('//span[text()="Arrangements : "]/following-sibling::a/text()').getall()
        item["tracklist"] = Selector(response).xpath('//table[@id="onglets_3_tracklist"]/tbody/tr/td[@class="cd_tracklist_titre"]/text()').getall()
        yield item
