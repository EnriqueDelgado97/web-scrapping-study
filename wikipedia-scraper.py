import requests
from lxml import html


if __name__ == '__main__':

    url ='https://www.wikipedia.org'
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    response = requests.get(url, headers=headers)

    parser = html.fromstring(response.text)
    
    for idioma in parser.xpath("//div[contains(@class,'central-featured-lang')]//strong/text()"):
        print(idioma)
