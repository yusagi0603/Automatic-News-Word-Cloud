from datetime import datetime

import jieba
import jieba.analyse
import logging
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import config
import crawler
# from web_crawler import crawler

''' Collect Data
'''
class NewsWordCloud():

    def __init__(self):
        self.date = datetime.today().strftime("%Y%m%d")

    def plot_word_cloud(self, news_df, category, stop_word_list=None):

        # build dict from news_df for wordcloud
        top_10 = news_df.article.apply(lambda x: jieba.analyse.extract_tags(' '.join(jieba.lcut(x)), topK=10, withWeight=True))
        text_seties = top_10.apply(lambda tfidf_list: [tfidf_tuple[0] for tfidf_tuple in tfidf_list])
        text = ' '.join([st for row in text_seties for st in row])
        
        # generate wordcloud and save plot
        stopwords = {}.fromkeys(stop_word_list)
        wc = WordCloud(font_path="font/NotoSerifCJKtc-Medium.otf", 
                    background_color="white", 
                    max_words = 2000 , 
                    random_state= 40,      
                    stopwords=stopwords) 
        wc.generate(text)
        wc.to_file('plot/set_{news_cate}_{date}.png'.format(
            news_cate=category, date=self.date))
        logging.info('Save Word Cloud Plot')

    def generate_cloud(self, keyword):

        # combine all df from source media
        target_cate = config.cate_trans.get(keyword) # chinese -> english
        cate_code = config.SET_cate.get(target_cate) # english -> number
        logging.info('Collect "{}" news from SET web'.format(target_cate))

        # plot and save word cloud
        web_url = 'https://www.setn.com/Catalog.aspx?PageGroupID={news_category}'.format(news_category=cate_code)
        news_df = crawler.get_set_news(web_url)

        with open('news_data/stopwords.txt', 'r',encoding='utf-8') as f:
            stop_word_list = f.read().split(' ')
            self.plot_word_cloud(news_df=news_df,
                    category=target_cate,
                    stop_word_list=stop_word_list)

if __name__ == "__main__":
    
    # set_cate = [('41', 'society'), ('4','daily'), ('5','global'), ('2','finace'), ('7', 'tech'), ('6','politics')]
    # set_url = [('https://www.setn.com/Catalog.aspx?PageGroupID={news_category}'.format(
    #     news_category=cate_code), cate_str) for cate_code, cate_str in set_cate]
    # for url, cate in set_url:
    # #     print(get_set_news(url))
    # # test_url = 'https://www.setn.com{href}'.format(href='/Catalog.aspx?PageGroupID=6')
    #     set_df = crawler.get_set_news(url)
    
    #     plot_word_cloud(set_df,
    #                     category=cate,
    #                     stop_word_list = ['或員工'])
    
    wordcloud = NewsWordCloud()
    wordcloud.generate_cloud(keyword='政治')