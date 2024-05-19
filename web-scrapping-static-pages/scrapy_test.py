from scrapy.item import Field, Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

class Pregunta(Item):
    """
    Se trata de los datos que YO quiero extraer cada campo o field se 
    corresponde con aquellos atributos que yo quiero extraer
    """
    id= Field()
    pregunta = Field()
    descripcion = Field()



class StackOverFlow(Spider):
    name = "MiPrimerSpider"
    start_urls = ['https://stackoverflow.com/questions']
    custom_settings = {
        'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    def parse(self, response):
        sel = Selector(response)
        questions = sel.xpath('//div[@id="questions"]//div[starts-with(@id, "question-summary")]')
        i =1
        for question in questions:
            item = ItemLoader(Pregunta(), question)
            item.add_xpath('pregunta','.//h3/a[@class="s-link"]/text()')
            item.add_xpath('descripcion', './/div[@class="s-post-summary--content-excerpt"]/text()')
            item.add_value('id',i)
            i +=1
            yield item.load_item()

if __name__ == '__main__':
    process = CrawlerProcess({
        'FEED_FORMAT': 'json',
        'FEED_URI': 'video.json'
        }
    )
    process.crawl(StackOverFlow)
    process.start()
