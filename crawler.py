import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_set_news(web_url):

    r = requests.get(web_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    hot_articles = soup.find_all('a', pl='熱門新聞')
    
    all_title = []
    all_url = []
    all_doc = []

    for article in hot_articles:
        
        article_url = 'https://www.setn.com{href}'.format(href=article.get('href'))
        article_soup = BeautifulSoup((requests.get(article_url)).text, 'html.parser')
        doc = ''.join([sent.text for sent in article_soup.find_all('div', id='Content1')])
        all_title.append(article.text)
        all_url.append(article_url)
        all_doc.append(doc)

    article_df = pd.DataFrame({'title': all_title, 'url': all_url, "article": all_doc})
    
    return article_df

def get_now_news(web_url): # undone 

    r = requests.get(web_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    hot_articles = soup.find_all('h3', class_='entry-title')
    
    print(hot_articles)
    all_title = []
    all_url = []
    all_doc = []

    for article in hot_articles:
        
        article_url = '{href}'.format(href=article.get('href'))
        article_soup = BeautifulSoup((requests.get(article_url)).text, 'html.parser')
        doc = ''.join([sent.text for sent in article_soup.find_all('div', id='Content1')])
        all_title.append(article.text)
        all_url.append(article_url)
        all_doc.append(doc)

    article_df = pd.DataFrame({'title': all_title, 'url': all_url, "article": all_doc})
    
    return article_df

if __name__ == '__main__':

    # set
    set_cate = ['41', '4', '5', '2', '7']
    set_url = ['https://www.setn.com/Catalog.aspx?PageGroupID={news_category}'.format(
        news_category=cate_code) for cate_code in set_cate]
    for url in set_url:
        print(get_set_news(url))

    # now
    now_url = 'https://www.nownews.com/cat/politics/'
    # get_now_news(now_url)