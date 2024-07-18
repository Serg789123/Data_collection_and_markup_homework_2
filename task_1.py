"""Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь информацию о всех книгах 
на сайте во всех категориях: название, цену, количество товара в наличии (In stock (19 available)) в формате 
integer, описание.Затем сохранить эту информацию в JSON-файле."""


import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, time, timedelta
import time
import re
import json


def information_about_books():
    books = []
    url = 'http://books.toscrape.com'
    # Отправка GET запроса на URL
    response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})
    # Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    release_links = [] # Список для хранения ссылок
    title_list = []
    for link in soup.find_all('article', ('class', 'product_pod')):
        release_links.append(link.find('a').get('href'))
        # наименование товара
        title = link.find('h3').a['title']
        title_list.append(title)



    url_joined = []  # Объединение ссылок с базовым URL-адресом для создания списка URL-адресов

    for link in release_links:
        url_joined.append(urllib.parse.urljoin('http://books.toscrape.com', link))

    for url in url_joined:
        response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})
        description_soup = BeautifulSoup(response.content, 'html.parser')
        
        # количество товара в наличии
        in_stock  = description_soup.find('p', ('class', 'instock availability')).text.strip()
        # цена товара
        price = description_soup.find('article', ('class', 'product_page')).find_all('p')[0].text[1:]
        #  описание товара
        description = description_soup.find('article',('class', 'product_page')).find_all('p')[3].text
    
        book = {
            'price': price,
            'in_stock': in_stock,
            'description': description
        }
        books.append(book)
        time.sleep(10)

    for i in range(0, len(title_list)):
        books[i].update({'title': title_list[i]})

    return books


def save_data_to_json(books, filename='box_office_data.json'):
    with open(filename, 'w') as f:
        json.dump(books, f, indent=4)


def main():
    books = information_about_books()
    save_data_to_json(books)

if __name__ ==  "__main__":
    main()