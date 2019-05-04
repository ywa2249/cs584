
import pandas as pd

#get relative result dataframe
from helperPython.relative_search import *
#get label result of query
from helperPython.question_labeler import *
#get ranking based on label
from helperPython.sort_prof import *
#get mix score
from helperPython.score_sum import *

pd.set_option('display.max_columns', 100)

def find_career_helper(query):
    #path of saved index for relative search
    store_index_path = 'store_index'
    #path of saved label information
    store_label_path = 'csvData/modified_professor_label_score.csv'
    #path of all saved answers
    saved_answer_path = 'csvData/answers.csv'

    #----- relative ranking -----#
    #preprocess query for relative ranking
    word_list = preprocess(query)
    tmp = ' '.join(word for word in word_list)
    relative_ranking_result = query_answer(store_index_path,tmp)

    #----- label ranking -----#
    #get the label
    label,second_label=label_question(query)

    #single label case
    if second_label==-1:
        label_ranking_result=find_prof(store_label_path, label, threshold=30)
    else:
        label_ranking_result=find_expert(store_label_path, label, second_label)

    #----- mix ranking ----#
    r_df=generate_relative_df(relative_ranking_result,100)
    r_df=add_relative_score(r_df)
    l_df=generate_label_df(label_ranking_result)

    mix_df=relative_and_label_sum(r_df,l_df,0.1,10)
    # print 'final result'
    # print mix_df

    best_pro_list=[]
    best_pro_list = mix_df["professionals_id"].tolist()

    return best_pro_list

def check_professor_past_answer(pid):
    # path of all saved answers
    pd.set_option('display.max_colwidth', 300)
    saved_answer_path = 'csvData/answers.csv'
    df = pd.read_csv(saved_answer_path)
    # print list(df)
    print df.loc[df['answers_author_id'] == pid]

if __name__ == '__main__':
    print "call careerHelper"
    query = 'How to apply an job in hospital or medical field? I am a biology master in Emory university'
    proList= find_career_helper(query)
    print proList

    #check_professor_past_answer(proList[2])
