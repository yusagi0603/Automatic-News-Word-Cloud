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
class WordClound():

    @classmethod
    def get_data(cls):

        web_config = config.NewsURL 
        reqs = []
        for news_name, news_config in web_config.iteritems(): # SET: {'url', 'hot_list_path'}, CNA: {}
            reqs.append(requests.get(news_config.get('url')))
            print
        reqs = list(requests.get())
        return cls()

    def __init__(self, text_dataframe):
        pass

    def plot_word_cloud(news_df, category, stop_word_list=None):

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
        wc.to_file('plot/set_{}.png'.format(category))
        logging.info('Save Word Cloud Plot')

    def generate_cloud(self):

        # combine all df from source media
        
        
        # plot and save word cloud

        pass

def plot_word_cloud(news_df, category, stop_word_list=None):

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
    wc.to_file('plot/set_{}.png'.format(category))
    logging.info('Save Word Cloud Plot')


if __name__ == "__main__":
    
    set_cate = [('41', 'society'), ('4','daily'), ('5','global'), ('2','finace'), ('7', 'tech'), ('6','politics')]
    set_url = [('https://www.setn.com/Catalog.aspx?PageGroupID={news_category}'.format(
        news_category=cate_code), cate_str) for cate_code, cate_str in set_cate]
    for url, cate in set_url:
    #     print(get_set_news(url))
    # test_url = 'https://www.setn.com{href}'.format(href='/Catalog.aspx?PageGroupID=6')
        set_df = crawler.get_set_news(url)
    
        plot_word_cloud(set_df,
                        category=cate,
                        stop_word_list = ['或員工'])
    
