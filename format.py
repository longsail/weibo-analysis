#coding=utf-8
import jieba
from collections import defaultdict
from collections import Counter
from gensim import corpora,models

def get_stopwords(filename='stopwords'):

    with open(filename,'r') as f:
        lines = f.readlines()
    stopwords = [line.replace("\r\n",'') for line in lines]
    stopwords = set(stopwords)
    return stopwords


def format(filename='audi.txt'):

    stopwords = get_stopwords()

    with open(filename,'r') as f:
        lines = f.readlines()
    
    texts = []
    for line in lines:
        line = line.replace('\n','')
        seg_list = jieba.cut(line)
        seg_list = [word.encode('utf-8') for word in seg_list]
        seg_list = [word for word in seg_list if word not in stopwords and len(word)>=4]
        texts.append(seg_list)

    all_tokens = sum(texts,[])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word)==1)
    texts = [[word for word in text if word not in tokens_once] for text in texts]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    return dictionary,corpus

if __name__ == "__main__":
    dictionary,corpus = format(filename='test.txt')
