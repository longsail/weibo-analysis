#coding=utf-8
import re
import jieba
import jieba.posseg as pseg
import itertools
from collections import defaultdict
from collections import Counter
from gensim import corpora,models


def get_stopwords(filename='stopwords'):

    with open(filename,'r') as f:
        lines = f.readlines()
    stopwords = [line.replace("\r\n",'') for line in lines]
    stopwords = set(stopwords)
    return stopwords

def format(filename='data.txt'):

    stopwords = get_stopwords()
    with open(filename,'r') as f:
        lines = f.readlines()
    texts = []
    postags = []
    for line in lines:
        line = line.replace('\n','')
        line = pseg.cut(line)

	wordslist = []
	for postag in line:
		flag = (postag.flag).encode('utf-8')
		word = (postag.word).encode('utf-8')
		if flag!='x' and len(word)>=4 and word not in stopwords:
			wordslist.append(word)
			postags.append(word+flag)
        texts.append(wordslist)

    #all_tokens = sum(texts,[])
    #tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word)==1)
    #texts = [[word for word in text if word not in tokens_once] for text in texts]
    return texts,postags

texts,postags = format(filename='test.txt')


def get_keyphrase(filename='data.txt'):
    postag_words = ' '.join(postags)
    regex = r'([\x80-\xff]+n [\x80-\xff]+n)'
    p = re.compile(regex)
    candidate_keyphrases = p.findall(postag_words)
    print 'keyphrase_list',len(candidate_keyphrases)
    candidate_keyphrases = [keyphrase.replace('n','') for keyphrase in candidate_keyphrases]
    print 'keyphrase happy'
    return candidate_keyphrases

def get_worddegree(filename='data.txt',window_size=5):
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

def record_lda(filename='data.txt',num_topics=3,update_every=0,passes=20):
	
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
    		inv_map = {v.encode('utf-8'):k for k,v in dict(wordtuple_list).items()}
    		topicword_distribution[i] = inv_map
    		i += 1
	return topic_distribution,topicword_distribution

if __name__ == "__main__":
	#test1,test2 = record_lda(filename='test.txt')
	#print test1,sum(test1.values())
	word_indegree,word_outdegree = get_worddegree(filename='test.txt')
	#print len(word_outdegree),len(word_indegree)
	#topicword_distribution = record_lda(filename='test.txt')[1]
	#count = 0
	#f#or i in range(0,3):
	#	for key in topicword_distribution[i]:
	#		if key not in word_outdegree.keys():
	#			print i,key
	#			count += 1
	#print count
	keyphrase_list = get_keyphrase(filename='test.txt')
	count = 0
	for keyphrase in keyphrase_list:
		words_list = keyphrase.split(' ')
		for word in words_list:
			if word not in word_outdegree.keys():
				count += 1
				print word
	print 'count',count

