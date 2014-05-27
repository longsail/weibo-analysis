#coding=utf-8
import operator
from collections import defaultdict
import jieba.posseg as pseg
import jieba
from format import record_lda
from format import get_worddegree

	

def wordrank(word_indegree,word_outdegree,word_distribution,daming_factor=0.85,max_iteration=100):
    nodes_num = len(word_distribution)
    wordrank = {word:1.0/nodes_num for word in word_distribution}
    for iteration in xrange(max_iteration):
        diff = 0.0
        for word in word_distribution:
            weight = 0.0
            for word_j in word_indegree[word]:
                out_degree = word_outdegree[word_j]
                weight += word_indegree[word][word_j]*1.0*word_distribution[word_j]/out_degree
            wordrank[word] = daming_factor*weight+(1-daming_factor)*word_disbution[word]
    return wordrank

def topicalPR(filename='data.txt'):
	topic_wordrank = defaultdict(defaultdict)
	word_indegree = get_worddgree(filename)[0]
	word_outdegree = get_worddgree(filename)[1]
	topic_worddistribution = record_lda(filename)[1]
	for topic in topic_worddistribution:
		topic_wordrank[topic] = wordrank(word_indegree,word_outdegree,topic_worddistribution[topic])
	return topic_wordrank

def get_keyphrase(filename='test.txt'):
    with open(filename,'r') as f:
        words = f.read()
    postag_words = pseg.cut(words)
    postag_words = ' '.join([(w.word).encode('utf-8')+(w.flag).encode('utf-8') for w in postag_words])
    regex = r'([\x80-\xff]+n [\x80-\xff]+n)'
    p = re.compile(regex)
    candidate_keyphrases = p.findall(postag_words)
    return candidate_keyphrases


def rank_keyphrase(keyphrase_list,filename='data.txt'):
	keyphrase_list = get_keyphrase(filename)
	topic_distribution = record_lda(filename)[0]
	topic_wordrank = topicalPR(filename)

	topic_keyphraserank = defaultdict(lambda:defaultdict(int))
	topic_list = topic_distribution.keys()
	for keyphrase in keyphrase_list:
		word_list = keyphrase.split(' ')
		for topic in topic_list:
			for word in word_list:
				topic_keyphraserank[topic][keyphrase] += topic_wordrank[topic][word]
    
   	keyphrase_rank = defaultdict(int)
	for keyphrase in keyphrase_list:
		keyphrase_weight = 0.0
        	for topic in topic_list:
            		keyphrase_weight += topic_keyphraserank[topic][keyphrase]*topic_distribution[topic]
        	keyphrase_rank[keyphrase] = keyphrase_weight
	return keyphrase_rank


if __name__ == "__main__":
    get_keyphrase()
