"""
Vamos a hacer scraping de la pagina de ign. 
Vamos a extraer información de los articulos juegos videos y reviews. 
Por cada uno de estos hay paginas (Horizontal)
"""
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

class Article(Item):
    """
    Se trata de los datos que YO quiero extraer cada campo o field se 
    corresponde con aquellos atributos que yo quiero extraer
    """
    titulo = Field()
    content = Field()

class Review(Item):
    """
    Se trata de los datos que YO quiero extraer cada campo o field se 
    corresponde con aquellos atributos que yo quiero extraer
    """
    titulo = Field()
    calificacion = Field()

class Video(Item):
    """
    Se trata de los datos que YO quiero extraer cada campo o field se 
    corresponde con aquellos atributos que yo quiero extraer
    """
    titulo = Field()
    date = Field()


class IGNCrawler(CrawlSpider):
    name = "NerdSpider"
    allowed_domains = ['latam.ign.com']
    start_urls = ['https://latam.ign.com/se/?model=article&q=ps5&order_by=']
    custom_settings = {
        'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    ## Vamos a visitar varias paginas por lo tanto vamos a insertar un delay para que scrapy pase por un usuario normal

    download_delay = 1

    ## Vamos a definir las rules
    """
    Rules:
    La primera es identificar las urls
    
    """
    rules = (
        #Horizontalidad por tipo de INFO
        Rule(
            LinkExtractor(
                allow = r'type='
            ), follow = True
        ),
        #Horizontalidad de paginacion
        Rule(
            LinkExtractor(
                allow = r'&page=\d+'
            ), follow = True
        ),

        Rule(
            LinkExtractor(
                allow = r'/review/'
            ), follow = True, callback= "parse_review"
        ),
        Rule(
            LinkExtractor(
                allow = r'/video/'
            ), follow = True, callback = "parse_video"
        ),
        Rule(
            LinkExtractor(
                allow = r'/news/'
            ), follow = True, callback = "parse_news"
        )

    )


    def parse_review(self, response):
        item = ItemLoader(Review(),response)
        item.add_xpath('titulo','//h1/text()')
        item.add_xpath('calificacion','//span[@class="side-wrapper side-wrapper hexagon-content"]')
        yield item.load_item()

    def parse_video(self, response):
        item = ItemLoader(Video(),response)
        item.add_xpath('titulo','//h1/text()')
        item.add_xpath('date','//span[@class="publish-date"]/text()')
        yield item.load_item()
    
    def parse_news(self, response):
        item = ItemLoader(Article(),response)
        item.add_xpath('titulo','//h1/text()')
        item.add_xpath('content','//div[@id="id_text"]//*/text()')
        yield item.load_item()

if __name__ == '__main__':
    process = CrawlerProcess({
        'FEED_FORMAT': 'json',
        'FEED_URI': 'ign.json'
        }
    )
    process.crawl(IGNCrawler)
    process.start()