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

def format(filename='data.txt'):

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
    return texts

def get_worddegree(filename='data.txt',window_size=5):
	texts = format(filename)
	wordlist = list(itertools.chain(*texts))
	length = len(wordlist)
	#wordgraph = [wordlist[i]+' '+wordlist[j] for i in range(length) for j in range(i+1,length-window_size)]
	word_dict = Counter(wordgraph)
	word_indegree = defaultdict(lambda:defaultdict(int))
	word_outdegree = defaultdict(int)
	for edge in word_dict:
		word_i = edge.split(' ')[0]
		word_j = edge.split(' ')[1]
		word_indegree[word_j][word_i] = word_dict[edge]
		word_outdegree[word_i] += word_dict[edge]
	return word_indegree,word_outdegree

def record_lda(filename='data.txt',num_topics=10,update_every=0,passes=20):
	
	texts = format(filename)
    	dictionary = corpora.Dictionary(texts)
    	corpus = [dictionary.doc2bow(text) for text in texts]
    	doc = list(itertools.chain(*corpus))
    	topic_corpus = []
    	topic_corpus.append(doc)

	word_num = len(dictionary)
	lda = models.ldamodel.LdaModel(corpus=corpus,id2word=dictionary,num_topics=num_topics,update_every=update_every,passes=passes)
	for topic_tuple in lda[topic_corpus]:
		topic_distribution = dict(topic_tuple)
	word_distribution = defaultdict(lambda:defaultdict(float))
	i = 0
	for wordtuple_list in lda.show_topics(topics=num_topics,topn=word_num,formatted=False):
    		inv_map = {v:k for k,v in dict(wordtuple_list).items()}
    		word_distribution[i] = inv_map
    		i += 1
	return topic_distribution,word_distribution

if __name__ == "__main__":
	test1,test2 = record_lda(filename='test.txt')
	print test1,test2
