import requests
from bs4 import BeautifulSoup

URL = 'https://habr.com'
KEYWORDS = ['Microsoft', 'Unreal', 'Qrator']

def get_request(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features='html.parser')
    return soup

def get_full_text(url):
    soup = get_request(url)
    article = soup.find('article')
    post_text = article.find(class_='article-formatted-body').text
    return post_text

def parser_posts(url, keywords):
    soup = get_request(url)
    articles = soup.find_all('article')
    for article in articles:
        hubs = article.find_all(class_='tm-article-snippet__hubs-item')
        hubs = " ".join([hub.find('span').text for hub in hubs])
        title = article.find('h2').text
        previews = article.find_all(class_='article-formatted-body')
        previews = " ".join([preview.text for preview in previews])
        link_full_post = article.find(class_='tm-article-snippet__readmore').get('href')
        full_post_text = get_full_text(URL+link_full_post)
        public_date = article.find('time').get('title')
        for search_word in keywords:
            if (search_word.lower() in hubs.lower()) or (search_word.lower() in title.lower()) or (search_word.lower() in previews.lower()) or (search_word.lower() in full_post_text.lower()):
                print(f'Дата: {public_date} - Заголовок: {title} - Ссылка: {URL}{link_full_post}')

if __name__ == '__main__':
    parser_posts(URL, KEYWORDS)