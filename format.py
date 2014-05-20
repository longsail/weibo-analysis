#coding=utf-8
import jieba
from collections import Counter

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
    
    with open('format.txt','w') as f:
        for line in lines:
            line = line.replace('\n','')
            seg_list = jieba.cut(line)
            seg_list = [word.encode('utf-8') for word in seg_list]
            seg_list = [word for word in seg_list if word not in stopwords and len(word)>=4]
            seg_dict = Counter(seg_list)
            string_to_file = ''
            for key in seg_dict:
                string_to_file += key+' '+str(seg_dict[key])+' '
            if string_to_file:
                f.write(string_to_file+'\n')

def get_wordgraph(filename='reply.txt',window_size=4):
    with open(filename,'r') as f:
        word_seq = f.read()

    seg_list = jieba.cut(word_seq)
    seg_list = [word.encode('utf-8') for word in seg_list]
    length = len(seg_list)
    word_graph = [seg_list[i]+' '+seg_list[i+j] for i in xrange(0,length-window_size) for j in xrange(1,window_size)]
    word_graph_dict = Counter(word_graph)

    with open('word_graph.txt','w') as f:
        for edge in word_graph_dict:
            weight = str(word_graph_dict[edge])
            f.write(edge+' '+weight+'\n')

if __name__ == "__main__":
    #format()
    get_wordgraph()
