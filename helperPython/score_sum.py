

import pandas as pd
import sys

#---- relative score zone----#
def generate_relative_df(df,max_line):
    cur_max_line=df.shape[0]
    if max_line<=cur_max_line:
        new_df=df.head(max_line)
    else:
        new_df=df
    return new_df

def add_relative_score(df):
    new_df=df[['professionals_id','score']]
    new_df=new_df.rename(columns={'score': 'r_score'})
    new_df.groupby(['professionals_id']).sum()
    return new_df

#---- label score zone ----#
def generate_label_df(df):
    new_df=df[['professionals_id','score1']]
    new_df=new_df.rename(columns={'score1':'l_score'})
    return new_df


#---- score sum zone ----#
def relative_and_label_sum(relative_df,label_df,alpha,top_n):
    sum_df=pd.merge(label_df,relative_df,how='left',on='professionals_id')
    sum_df.fillna(0)
    sum_df['weight_sum']=sum_df['r_score']*alpha+sum_df['l_score']*(1-alpha)
    sum_df.sort_values(by=['weight_sum'])
    return sum_df.head(top_n)



# def test_best_alpha():
#     alpha_list=[0.1,0.3,0.5,0.7,0.9]
#     for i in range(len(alpha_list)):
#         sum_df=relati

if __name__ == '__main__':
    print sys.path
    print "call score sum"