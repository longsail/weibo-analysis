#coding=utf-8
import jieba
from collections import defaultdict
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

def get_wordindex(filename='format.txt'):

    with open(filename,'r') as f:
        lines = f.readlines()
        
    wordlist = []
    for line in lines:
        line = line.replace('\n','')
        line = line.split(' ')
        line = filter(None,line)
        for word in line:
            wordlist.append(word)
    wordlist = list(set(wordlist))
    wordindex = {word:index for index,word in enumerate(wordlist)}
    
    with open(filename,'r') as f:
        line = f.readlines()

    f = open('lda_format.txt','w')
    for line in lines:
        line = line.replace('\n','')
        line = line.split(' ')
        line = filter(None,line)
        word_dict = Counter(line)
        count = len(word_dict)
        string_to_file = ''
        for word in word_dict:
            string_to_file += str(wordindex[word])+' '+str(word_dict[word])+' '
        if string_to_file:
            f.write(str(count)+' '+string_to_file+'\n')
    f.close()

if __name__ == "__main__":
    format(filename='test.txt')
    get_wordindex(filename='format.txt')
