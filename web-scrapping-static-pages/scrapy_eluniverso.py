from scrapy.item import Field, Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup

class Noticia(Item):
    titular = Field()
    #id = Field()
    #descripcion = Field()


class ElUniverso(Spider):
    name = "MiSegundoSpider"
    start_urls = ['https://www.eluniverso.com/deportes/']
    custom_settings = {
        'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        contenedor_noticias = soup.find_all('div',class_='content-feed | space-y-2  ')
        for contenedor in contenedor_noticias:
            noticias = contenedor.find_all('li',class_='relative ',recursive = False)
            for new in noticias:
                print(new)
                item = ItemLoader(Noticia(),response.body)
                titular = new.find('h2').find('a').text
                item.add_value('titular', titular)
                yield item.load_item()
       
       

       
       
       
       
       
       
       
       
       
       
        #sel = Selector(response)
        #news = sel.xpath('//div[@class="content-feed | space-y-2  "]//li[@class="relative "]')
        #i = 1
        #for new in news:
        #    item = ItemLoader(Noticia(), new)
        #    item.add_xpath('titular','.//h2/a[@class="no-underline"]/text()')
        #    item.add_xpath('descripcion', './/p[@class="summary | text-sm m-0 font-secondary"]/text()')
        #    item.add_value('id',i)
        #    i +=1
        #    yield item.load_item()
