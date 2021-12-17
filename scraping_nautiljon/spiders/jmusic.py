import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


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
        yield scrapy.Request(url='https://www.nautiljon.com/jmusic/?q=z', headers={
            'User-Agent': self.user_agent
    })

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//td/span[@class="fright"]/following-sibling::a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//p[@class="menupage"][1]/a[text()=">|"]'), follow=True),
    )

    def parse_item(self, response):
        item = {}
        item["title"] = response.xpath('//h1/span[@itemprop="name"]/text()').get()
        item["type"] = response.xpath('//span[text()="Type : "]/following-sibling::text()').get()
        item["release_date"] = response.xpath('//span[@itemprop="datePublished"]/text()').get()
        item["label"] = response.xpath('//span[@itemprop="legalName"]/text()').get()
        item["producer"] = response.xpath('//span[text()="Distributeur : "]/following-sibling::a/text()').get()
        item["artists"] = response.xpath('//span[@itemprop="byArtist"]/text()').getall()
        item["lyrics"] = response.xpath('//span[text()="Paroles : "]/following-sibling::a/text()').getall()
        item["composers"] = response.xpath('//span[text()="Compositeurs : "]/following-sibling::a/text()').getall()
        item["arrangers"] = response.xpath('//span[text()="Arrangements : "]/following-sibling::a/text()').getall()
        item["tracklist"] = response.xpath('//table[@id="onglets_3_tracklist"]/tbody/tr/td[@class="cd_tracklist_titre"]/text()').getall()
        return item
