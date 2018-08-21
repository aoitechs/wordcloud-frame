# -*- coding: UTF-8 -*-

import re, jieba
from wordcloud import WordCloud

# format chatlog
chatlog = ''
for line in open('raw_chatlog.txt', 'r', encoding='utf-8'):
    # REMOVE: @someone emoji picture
    line = re.sub(r'(\@[^\s]*\s)|(\[.{2}\])', '', line)
    # REMOVE: web link
    line = re.sub(r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', '', line)
    # timestamp
    if (re.search(r'(^201\d)|(^$)', line) != None):
        continue
    chatlog += line[:-1]

# deal with specific noun
user = open('user.txt', 'w', encoding='utf-8')
for line in open('replace_pattern.txt', 'r', encoding='utf-8'):
    name_list = re.findall(r'([\u4E00-\u9FA5A-Za-z0-9]+)', line)
    for name in name_list:
        chatlog = re.sub(name, name_list[0], chatlog)
    user.write(name_list[0] + '\n')
user.close()

# readin stopwords
stopwords = []
for word in open('stopwords.txt', 'r', encoding='utf-8'):
    stopwords.append(word[:-1])

# split words
jieba.load_userdict('user.txt')
word_split =' '.join(jieba.cut(chatlog, cut_all=False))

# generate word cloud image
wordcloud = WordCloud(background_color='white', font_path="/Library/Fonts/simsun.ttc", \
width=1024,height=768,stopwords=stopwords,collocations=False,prefer_horizontal=1).generate(word_split)
wordcloud.to_file('wordcloud.jpg')
