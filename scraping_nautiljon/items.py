# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapingNautiljonItem(scrapy.Item):
    title = scrapy.Field()
    type = scrapy.Field()
    release_date = scrapy.Field()
    label = scrapy.Field()
    producer = scrapy.Field()
    artists = scrapy.Field()
    lyrics = scrapy.Field()
    composers = scrapy.Field()
    arrangers = scrapy.Field()
    tracklist = scrapy.Field()