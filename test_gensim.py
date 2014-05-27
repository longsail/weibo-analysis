import logging
from collections import defaultdict
from gensim import corpora,models,similarities
import itertools
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)
documents = ["Human machine interface for lab abc computer applications",
        "A survey of user opinion of computer system response time",
        "The EPS user interface management system",
        "System and human system engineering testsing of EPS",
        "Relation of user perceived response time to error measurement",
        "The generation of random binary unordered trees",
        "The intersection graph of paths in trees",
        "Graph minors IV Widths of trees and well quasi ordering",
        "Graph minors A survey"]
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
all_tokens = sum(texts,[])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word)==1)
texts = [[word for word in text if word not in tokens_once] for text in texts]
dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict')
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/deerwester.mm',corpus)
mm = corpora.MmCorpus('/tmp/deerwester.mm')
lda = models.ldamodel.LdaModel(corpus=mm,id2word=dictionary,num_topics=2,update_every=0,passes=10)
test = list(itertools.chain(*texts))
other_corpus = [dictionary.doc2bow(text) for text in test]
print other_corpus
print lda(other_corpus)
word_distribution = defaultdict(lambda:defaultdict(float))
i = 0
for wordtuple_list in lda.show_topics(topics=2,topn=12,formatted=False):
    inv_map = {v:k for k,v in dict(wordtuple_list).items()}
    word_distribution[i] = inv_map
    i += 1
#print word_distribution

    
