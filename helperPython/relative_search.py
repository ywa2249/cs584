from whoosh.qparser import QueryParser
from whoosh import index
import gensim
from nltk.stem import WordNetLemmatizer, SnowballStemmer
import nltk
from whoosh import scoring
nltk.download('wordnet')

import pandas as pd


def lemmatize_stemming(text):
    stemmer = SnowballStemmer('english')
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        #print 'token:',token
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            #print 'lemm:',lemmatize_stemming(token)
            result.append(lemmatize_stemming(token))
    return result

def query_answer(dir_name, query):
    ix = index.open_dir(dir_name)
    hits = []
    # query = 'I want to be a data scientists.'
    # prof_id = '54539d99e4304cf0a18357bab287dcf1'
    # parser = MultifieldParser(["answers_body","answers_author_id"], schema=ix.schema)
    parser = QueryParser('answers_body', schema=ix.schema)
    try:
        word = parser.parse(query)
    except:
        word = None

    if word is not None:
        s = ix.searcher(weighting=scoring.BM25F(B=0.75, title_B=10, content_B=1, K1=1.5))
        # s = ix.searcher(weighting=scoring.TF_IDF())
        hits = s.search(word, limit=10000)

        id_list = []
        answers_id_list = []
        answer_list = []
        score_list = []

        for hit in hits:
            id_list.append(hit['answers_author_id'])
            answers_id_list.append(hit['answers_id'])
            answer_list.append(hit['answers_body'])
            score_list.append(hit.score)

        query_result = pd.DataFrame(
            {'professionals_id': id_list, 'answers_id': answers_id_list, 'answers_body': answer_list,
             'score': score_list})

        return query_result
    else:
        print('Paser Fails.')
        return None


if __name__ ==  "__main__":
    # dir_name = 'answers'
    # pd.set_option('display.max_columns', 100)
    # query = 'I want to be a data scientist.'
    # word_list = preprocess(query)
    # tmp = ' '.join(word for word in word_list)
    # query_result = query_answer(dir_name,tmp)
    # print(query_result)
    print 'enter relative_search'