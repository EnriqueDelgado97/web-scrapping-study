import requests
from bs4 import BeautifulSoup




if __name__ =='__main__':

    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    url = 'https://stackoverflow.com/questions'
    respuesta = requests.get(url,headers=headers)
    soup = BeautifulSoup(respuesta.text)
    contenedor_de_preguntas = soup.find(id='questions')
    for question in contenedor_de_preguntas.find_all('div',class_='s-post-summary js-post-summary'):
        print('question:',question.find('h3').find('a',class_='s-link').text)
        print('summary:',question.find('div',class_='s-post-summary--content-excerpt').text.replace('\n','').replace('\r','').strip())
 