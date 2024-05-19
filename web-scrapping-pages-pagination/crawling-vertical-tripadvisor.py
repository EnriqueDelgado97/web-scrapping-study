from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess


class Bar(Item):
    """
    Se trata de los datos que YO quiero extraer cada campo o field se 
    corresponde con aquellos atributos que yo quiero extraer
    """
    nombre = Field()
    puntuacion = Field()
    #latitud = Field()
    #longitud = Field()
    direccion = Field()

class TripAdvisorSpider(CrawlSpider):
    name = "DrunkSpider"
    start_urls = ['https://www.tripadvisor.com/Restaurants-g187518-Murcia.html']
    custom_settings = {
        'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    ## Vamos a visitar varias paginas por lo tanto vamos a insertar un delay para que scrapy pase por un usuario normal

    download_delay = 2

    ## Vamos a definir las rules
    """
    Rules:
    La primera es identificar las urls
    
    """
    rules = (
        Rule(
            LinkExtractor(
                allow = r'/Restaurant_Review-'
            ), follow = True, callback = "parse_baretos"
        ),
    )
    def parse_baretos(self, response):
        sel = Selector(response)
        item = ItemLoader(Bar(),sel)

        item.add_xpath('nombre','//h1/text()')
        item.add_xpath('puntuacion','//div[@data-automation="reviewBubbleScore"]/text()')
        item.add_xpath('direccion','/a[@target="_blank"][1]/span/text()')
        yield item.load_item()

if __name__ == '__main__':
    process = CrawlerProcess({
        'FEED_FORMAT': 'json',
        'FEED_URI': 'bares.json'
        }
    )
    process.crawl(TripAdvisorSpider)
    process.start()