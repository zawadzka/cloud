import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from migration.items import MigrationItem
from migration.items import DrugiItem



from readability.readability import Document
import urllib
import html2text

class newCrawler(CrawlSpider):
    name='pit'
    allowed_domains = ['pit.pl']
    start_urls = ['http://www.pit.pl']
    rules = (
        Rule(LinkExtractor(allow=(), deny=(['.*\?.*','.*module.*','.*page.*','.*deklaracje_.*','.*att.*']), canonicalize=True, unique=True),
             callback="parse_items",
             follow=True),)
    def parse_items(self, response):
        item = DrugiItem()
        item['url']=response.url

        converter = html2text.HTML2Text()
        converter.ignore_links = True
        item['text']=converter.handle(response.css('section.lev2').extract_first())
        item['h1']=converter.handle(response.css('h1').extract_first())

        return item
