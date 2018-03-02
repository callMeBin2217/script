__author__='callMeBin'
#!/usr/bin/env Python
# coding=utf-8

import re
import requests
import jieba
import numpy as np
import codecs
import matplotlib
from bs4 import BeautifulSoup
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
import pandas as pd
import time
from pandas import Series,DataFrame
import getpass
from collections import Counter	


def makeWordCloud():
	sys_name = getpass.getuser()
	target_file = 'wyComment2.txt'
	with open(r'C:/Users/'+sys_name+'/Desktop/'+target_file,'r',encoding='utf-8') as f:
		data = f.read()
		pattern = re.compile(r'[\u4e00-\u9fa5a-zA-Z0-9].*')
		data = re.findall(pattern,data)
	#print(data)
	#使用结巴分词进行中文分词
	#jieba.add_word('白色球鞋')
	segment = jieba.lcut(str(data))
	print(Counter(segment)['吴佳怡'])
	words_df = DataFrame({'segment':segment})
	print(words_df)
	#去掉停用词,quoting=3全不引用
	stopwords = pd.read_csv(r'C:/Users/'+sys_name+'/Desktop/stopwords.txt',index_col=False,quoting=3,sep='\t',names=['stopword'],encoding='utf-8')
	words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
	#统计词频
	words_stat = words_df.groupby(by=['segment'])['segment'].agg({'计数':np.size})
	words_stat = words_stat.reset_index().sort_values(by=['计数'],ascending=False)
	#用词云进行显示
	back_img = plt.imread(r'C:/Users/'+sys_name+'/Desktop/color.jpg')
	img_color = ImageColorGenerator(back_img)
	wordcloud = WordCloud(mask=back_img,font_path='simhei.ttf',background_color='white',max_font_size=200,min_font_size=20,random_state=42,max_words=500)
	word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}


	wordcloud = wordcloud.fit_words(word_frequence)
	plt.axis('off')
	plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)
	plt.imshow(wordcloud.recolor(color_func=img_color))

def main():
	makeWordCloud()

if __name__ =='__main__':
	main()