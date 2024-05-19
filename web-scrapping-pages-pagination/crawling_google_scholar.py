"""
Vamos a hacer scraping de la pagina de google scholar. 
Vamos a extraer información de los articulos y visitaremos los articulos citados. 
Por cada uno de estos hay paginas (Horizontal)
"""
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

class Paper(Item):
    """
    Se trata de los datos que YO quiero extraer cada campo o field se 
    corresponde con aquellos atributos que yo quiero extraer
    """
    titulo = Field()
    authors = Field()
    citations = Field()
    url = Field()

class GoogleScholar(CrawlSpider):
    name = "GoogleSpider"
    allowed_domains = ['scholar.google.es']
    start_urls = ['https://scholar.google.es/scholar?hl=es&as_sdt=0%2C5&q=Covalent+organic+frameworks&btnG=']
    custom_settings = {
        'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    download_delay = 2

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths='//div[@class="gs_ri"]',
                allow=r'\?cites='
            ), follow=True, callback="parse_papers"
        ),

    )
    
    def parse_papers(self, response):
        sel = Selector(response)
        papers = sel.xpath('//div[@class="gs_ri"]')
        
        for paper in papers:
            item = ItemLoader(Paper(),paper)
            titulo = paper.xpath('.//h3/a//text()').get()
            url = paper.xpath('//h3/a/@href').get()
            

            authors = paper.xpath('.//div[@class="gs_a"]//text()').getall()
            authors = "".join(authors).split('-')[0].strip()
            try:
                citations = paper.xpath('.//a[contains(@href,"cites")]/text()').get()
                citations = citations.replace('Citado por','')
            except:
                citations = '0'
            
            item.add_value('titulo',titulo)
            item.add_value('url',url)
            item.add_value('authors',authors)
            item.add_value('citations', citations)
            
            yield item.load_item()

if __name__ == '__main__':
    process = CrawlerProcess({
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'papers.csv'
        }
    )
    process.crawl(GoogleScholar)
    process.start()