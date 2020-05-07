import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = str(soup.find('div', class_='paginator').find_all('a')[-2].get('href'))
    total_pages = pages.split('=')[-1]
    return int(total_pages)

def write_csv(data):
    with open('avto.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'], data['descrip'], data['price'], data['url']))

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='all-items-block content-section').find_all('div', class_='list-item')
    
    for ad in ads:
        try:
            title = ad.find('div', class_='item-title').text
        except:
            title = ''

        try:
            url = 'https://ru.autogidas.lt' + ad.find('a', class_='item-link').get('href')
        except:
            url = ''

        try:
            descrip = ad.find('div', class_='item-description').text
        except:
            descrip = ''

        try:
            price = ad.find('div', class_="item-price").text.strip()
        except:
            price = ''

        data = {'title': title,
                'descrip': descrip,
                'price': price,
                'url': url}

        write_csv(data)

def main():
    url = 'https://ru.autogidas.lt/skelbimai/automobiliai/?f_215=150&f_216=3000&f_41=2000&f_42=2020'

    base_url = 'https://ru.autogidas.lt/skelbimai/automobiliai/?f_215=150&f_216=3000&f_41=2000&f_42=2020'
    page_part = '&f_50=kaina_asc&page='

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i)

        html = get_html(url_gen)
        get_page_data(html)

if __name__ == '__main__':
    main()
