#coding=utf-8
import re
import operator
import itertools
from collections import defaultdict
import jieba.posseg as pseg
import jieba
from format import record_lda
from format import get_worddegree
from format import get_keyphrase

topic_distribution,topic_worddistribution = record_lda(filename='test.txt')

def rank_word(word_distribution,word_indegree,word_outdegree,daming_factor=0.85,max_iteration=100):
    for word in word_distribution:
	    if word not in word_outdegree.keys():
		    print 'not'
    
    word_num = len(word_distribution)
    wordrank = {word:1.0/word_num for word in word_distribution}
    for iteration in xrange(0,max_iteration):
        for word in word_distribution:
            weight = 0.0
            for word_j in word_indegree[word]:
                out_degree = word_outdegree[word_j]
		weight1 = word_indegree[word][word_j]
                weight += 1.0*weight1*wordrank[word_j]/out_degree
	    wordrank[word] = daming_factor*weight+(1-daming_factor)*word_distribution[word]
    print 'happy' 
    return wordrank

def topicalPR(filename='data.txt'):
	topic_wordrank = defaultdict(defaultdict)
	word_indegree,word_outdegree = get_worddegree(filename)
	#topic_worddistribution = record_lda(filename)[1]
	for topic in topic_worddistribution:
		topic_wordrank[topic] = rank_word(topic_worddistribution[topic],word_indegree,word_outdegree)
	return topic_wordrank


def rank_keyphrase(filename='data.txt'):
	keyphrase_list = get_keyphrase(filename)
	topic_wordrank = topicalPR(filename)

	topic_keyphraserank = defaultdict(lambda:defaultdict(int))
	topic_list = topic_distribution.keys()
	for keyphrase in keyphrase_list:
	    word_list = keyphrase.split(' ')
            weight = 0.0
	    for topic in topic_list:
		for word in word_list:
                    weight += topic_wordrank[topic][word]
	    topic_keyphraserank[topic][keyphrase] += weight
    
   	keyphrase_rank = defaultdict(int)
	for keyphrase in keyphrase_list:
		keyphrase_weight = 0.0
        	for topic in topic_list:
            		keyphrase_weight += topic_keyphraserank[topic][keyphrase]*topic_distribution[topic]
        	keyphrase_rank[keyphrase] = keyphrase_weight
        sorted_keyphrase = sorted(keyphrase_rank.iteritems(),key=operator.itemgetter(1),reverse=True)
        final_keyphrase = sorted_keyphrase[0:50]
        with open('keyphrase.txt','w') as f:
            for keyphrase in final_keyphrase:
                f.write(str(keyphrase[0])+','+str(keyphrase[1])+'\n')


if __name__ == "__main__":
	rank_keyphrase(filename='test.txt')
