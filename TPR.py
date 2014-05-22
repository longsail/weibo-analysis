#coding=utf-8
import operator
from collections import defaultdict
import jieba.posseg as pseg
from format import get_worddgree

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

def topicalPR():
	topic_wordrank = defaultdict(defaultdict)
	word_indegree = get_worddgree[0]
	word_outdegree = get_worddgree[1]
	topic_worddistribution = 
	for topic in topic_worddistribution:
		topic_wordrank[topic] = wordrank(word_indegree,word_outdegree,topic_worddistribution[topic])
	return topic_wordrank

#def get_keyphrase(wordrank_topic,number=100):
#   topic_keyphrase = {}
#    for topic in wordrank_topic:
#        wordrank = wordrank_topic[topic]
#        sort_wordrank = sorted(wordrank.iteritems(),key=operator.itemgetter(1),reverse=True)
#        topK_keyword = [item[1] for item in sort_wordrank[0:number]]
#        for i in xrange(0,100):
#            for j in xrange(0,100):
#                keyphrase = topK_keyword[i]+' '+topK_keyword[j]
#                topic_keyphrase[topic].append(keyphrase)
#        topic_keyphrase[topic] = list(set(topic_keyphrase[topic]))
#    return topic_keyphrase
 
def get_keyphrase(filename='test.txt'):
    with open(filename,'r') as f:
        words = f.read()
    postag_words = pseg.cut(words)
    postag_words = ' '.join([(w.word).encode('utf-8')+(w.flag).encode('utf-8') for w in postag_words])
    regex = r'([\x80-\xff]+n [\x80-\xff]+n)'
    p = re.compile(regex)
    candidate_keyphrases = p.findall(postag_words)
    return candidate_keyphrases


def rank_keyphrase(keyphrase_list,topic_wordrank):

	topic_keyphraserank = defaultdict(lambda:defaultdict(int))
	topic_list = topic_wordrank.keys()
	for keyphrase in keyphrase_list:
		word_list = keyphrase.split(' ')
		for topic in topic_list:
			for word in word_list:
				topic_keyphraserank[topic][keyphrase] += topic_wordrank[topic][word]
    
   	keyphrase_rank = defaultdict(int)
	for keyphrase in keyphrase_list:
		keyphrase_weight = 0.0
        	for topic in topics:
            		keyphrase_weight += topic_keyphraserank[topic][keyphrase]*pro(Z|D)
        	keyphrase_rank[keyphrase] = keyphrase_weight
	return keyphrase_rank

 #   return keyphrase_rank
#def rank_keyphrase(topic_keyphrase,wordrank_topic):
#    topic_keyphrase_rank = {}
#    for topic in topic_keyphrase:
#        for keyphrase in topic_keyphrase[topic]:
#            for word in keyphrase:
#                topic_keyphrase_rank[topic][keyphrase] += wordrank_topic[topic][word]
    
#    keyphrase_rank = {}
#    for keyphrase in keyphrase_list:
#        for topic in topics:
#            keyphrase_weight += keyphrase_rank_topic[topic][keyphrase]*pro(Z|D)
#        keyphrase_rank[keyphrase] = keyphrase_weight

 #   return keyphrase_rank


if __name__ == "__main__":
    get_keyphrase()
