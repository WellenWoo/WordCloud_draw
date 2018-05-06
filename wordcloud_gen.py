# -*-encoding:utf-8 -*-

from os import path
from PIL import Image
import numpy as np
import time
from wordcloud import WordCloud, STOPWORDS
import jieba

def user_stopwords(stopword_path):
    '''合并系统默认停用词与用户自定义停用词'''
    stopwords_sys = set(STOPWORDS)

    '''读取用户自定义停用词'''
    with open(stopword_path,'r') as f_stop:
        f_stop_text = f_stop.read()
        f_stop_seg_list = f_stop_text.split('\n')
    f_stop_seg_set = set(f_stop_seg_list)

    stopwords = stopwords_sys.union(f_stop_seg_set)
    return stopwords

def get_text(fn):
    text = open(fn).read()
    return text

def get_text_cn(fn):
    t0 = get_text(fn)
    t0 = jieba.cut(t0,cut_all = False)
    text = " ".join(t0)
    return text

def draw_wc(text,mask_path,stopwords):
    '''args:text,*mask,*stopwords'''
    mask = np.array(Image.open(mask_path))
                        
    wc = WordCloud(max_words = 1000,mask = mask,stopwords = stopwords,
                   margin = 0,random_state=1).generate(text)
    im = wc.to_image()
    im.show()
    fn = str(int(time.time()))+'.jpg'
    im.save(fn)
    return im
