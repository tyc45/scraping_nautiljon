import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class JmusicSpider(CrawlSpider):
    name = 'jmusic'
    allowed_domains = ['https://www.nautiljon.com/']
    start_urls = ['https://www.nautiljon.com/jmusic/?q=z']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        item["title"] = response.xpath('//span[text()="Titre original : "]/following-sibling::text()').get()
        item["type"] = response.xpath('//span[text()="Type : "]/following-sibling::text()').get()
        item["release_date"] = response.xpath('//span[@itemprop="datePublished"]/text()').get()
        item["label"] = response.xpath('//span[@itemprop="legalName"]/text()').get()
        item["producer"] = response.xpath('//span[text()="Distributeur : "]/following-sibling::a/text()').get()
        item["artists"] = response.xpath('//span[@itemprop="byArtist"]').getall()
        item["lyrics"] = response.xpath('//span[text()="Paroles : "]/following-sibling::a/text()"]').getall()
        item["composers"] = response.xpath('//span[text()="Compositeurs : "]/following-sibling::a/text()').getall()
        item["arrangers"] = response.xpath('//span[text()="Arrangements : "]/following-sibling::a/text()').getall()
        item["tracklist"] = response.xpath('//table[@id="onglets_3_tracklist"]/tbody/tr/td[@class="cd_tracklist_titre"]').getall()
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
