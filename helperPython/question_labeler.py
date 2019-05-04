
import pickle

import gensim
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *

from gensim import corpora, models
import nltk
nltk.download('wordnet')


def lemmatize_stemming(text):
    stemmer = SnowballStemmer('english')
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result


def get_highest_label(text,dic,clf,topic_list):
    label=-1
    #firstScore=0
    second_label=-1
    unseen_document = text
    # print preprocess(unseen_document)
    bow_vector = dic.doc2bow(preprocess(unseen_document))
    # print bow_vector
    counter=0
    for index, score in sorted(clf[bow_vector], key=lambda tup: -1 * tup[1]):
        # print("Score: {}\t Topic: {}".format(score, clf.print_topic(index, 5)))
        topic = clf.print_topic(index, 5)
        # print topic
        for index, str in enumerate(topic_list):
            sub = topic
            if str.find(sub) != -1:
                label=index
                break
        break

    return label,second_label




def highlight_tag(text):
    text=text+' '
    c = r"(?<=#)(.+?)(?=\ )"
    taglist= re.findall(c, text)
    new_text=text
    for word in taglist:
        new_text = new_text + (word + " ") * 4
    return new_text

def get_store_topic_list(path):
    topic_path = path
    txt = open(topic_path, 'r')

    txt_list = []
    for line in txt.readlines():
        line = line.strip()
        txt_list.append(str(line))
    #print(txt_list)
    txt.close()
    return txt_list


def label_question(text):
    #print 'input question:',text
    text=highlight_tag(text)
    # prepare topic_list, dictionary, model
    topic_list = get_store_topic_list('otherData/topicword100.txt')
    dictionary = corpora.Dictionary.load("otherData/dictionary1.dic")
    dictionary.filter_extremes(no_below=5, no_above=0.1, keep_n=10000)
    #print 'load model'
    with open('otherData/lda_tf_100topic.pickle', 'rb') as f:
        lda_tf = pickle.load(f)
    label = get_highest_label(text, dictionary, lda_tf, topic_list)
    #print 'label:', label

    return label



if __name__ == '__main__':
    label_question('sample')

