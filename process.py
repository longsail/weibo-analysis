#!/usr/bin/env python
#coding=utf-8
import re
import sys
import itertools
from collections import defaultdict,Counter
try:
    import jieba
    import jieba.posseg as pseg
    from gensim import corpora,models

except ImportError:
        print >> sys.stderr, """\

There was a problem importing one of the Python modules required.
The error leading to this problem was:

%s

Please install a package which provides this module, or
verify that the module is installed correctly.

It's possible that the above module doesn't match the current version of Python,
which is:

%s

""" % (sys.exc_info(), sys.version)
        sys.exit(1)


def get_stopwords(filename='stopwords'):

    with open(filename,'r') as f:
        lines = f.readlines()
    
    stopwords_list = [line.replace("\r\n",'') for line in lines]
    stopwords = set(stopwords_list)
   
    return stopwords

def format(filename='data.txt'):

    stopwords = get_stopwords()
    
    with open(filename,'r') as f:
        lines = f.readlines()
    texts = []
    postag_list = []
    for line in lines:
        line = line.replace('\n','')
        line = pseg.cut(line)

	wordslist = []
	for postag in line:
		flag = (postag.flag).encode('utf-8')
		word = (postag.word).encode('utf-8')
		if flag!='x' and len(word)>=4 and word not in stopwords:
			wordslist.append(word)
			postag_list.append(postag)
        texts.append(wordslist)

    all_tokens = sum(texts,[])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word)==1)
    texts = [[word for word in text if word not in tokens_once] for text in texts]
    postags = []
    for postag_word in postag_list:
        if (postag_word.word).encode('utf-8') not in tokens_once:
            postags.append((postag_word.word).encode('utf-8')+(postag_word.flag).encode('utf-8'))
    return texts,postags


def get_keyphrase(postags):
    postag_words = ' '.join(postags)
    regex = r'([\x80-\xff]+n [\x80-\xff]+n)'
    p = re.compile(regex)
    
    candidate_keyphrases = p.findall(postag_words)
    candidate_keyphrases = [keyphrase.replace('n','') for keyphrase in candidate_keyphrases]
    
    return candidate_keyphrases

def get_worddegree(texts,window_size=5):

	wordlist = list(itertools.chain(*texts))
	length = len(wordlist)
	wordgraph = [wordlist[i]+' '+wordlist[i+j] for i in range(0,length) for j in range(1,window_size) if i+j<length]
	word_dict = Counter(wordgraph)
	word_indegree = defaultdict(lambda:defaultdict(int))
	word_outdegree = defaultdict(int)
	for edge in word_dict:
		word_i = edge.split(' ')[0]
		word_j = edge.split(' ')[1]
		word_indegree[word_j][word_i] = word_dict[edge]
		word_outdegree[word_i] += word_dict[edge]
	return word_indegree,word_outdegree

def record_lda(texts,num_topics=10,update_every=0,passes=20):
	
    	dictionary = corpora.Dictionary(texts)
    	corpus = [dictionary.doc2bow(text) for text in texts]
    	doc = list(itertools.chain(*corpus))
    	topic_corpus = []
    	topic_corpus.append(doc)

	word_num = len(dictionary)

	lda = models.ldamodel.LdaModel(corpus=corpus,id2word=dictionary,num_topics=num_topics,update_every=update_every,passes=passes)
	for topic_tuple in lda[topic_corpus]:
		topic_distribution = dict(topic_tuple)
	
	topicword_distribution = defaultdict(lambda:defaultdict(float))
	i = 0
	for wordtuple_list in lda.show_topics(topics=num_topics,topn=word_num,formatted=False):
    		inv_map = {v:k for k,v in dict(wordtuple_list).items()}
    		topicword_distribution[i] = inv_map
    		i += 1
	return topic_distribution,topicword_distribution

def process_file(filename='data.txt'):
    
    texts,postags = format(filename=filename)
    keyphrases = get_keyphrase(postags=postags)
    word_indegree,word_outdegree = get_worddegree(texts)
    topic_distribution,topicword_distribution = record_lda(texts)

    return keyphrases,word_indegree,word_outdegree,topic_distribution,topicword_distribution

if __name__ == "__main__":
    keyphrases,word_indegree,word_outdegree,topic_distribution,topicword_distribution = process_file(filename='test1.txt')
    print len(word_indegree),len(word_outdegree),len(topicword_distribution[0])
    count = 0
    for keyphrase in keyphrases:
        word_list = keyphrase.split(' ')
        for word in word_list:
            if word not in word_outdegree.keys():
                print 'not'
                count += 1
    print count
