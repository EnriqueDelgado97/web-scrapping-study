import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'https://news.ycombinator.com'
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    respuesta = requests.get(url, headers=headers)
    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.text)
        for item in soup.find_all('tr',class_ ='athing'):
            for element in item.find_all('td',class_='title'):
                print(element.find('span',class_='titleline').find('a'))#.find('td',class_='title'))

