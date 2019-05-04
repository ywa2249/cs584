import pandas as pd
import numpy as np


# path: csv file path ('label_score.csv')
# label_1: find the professor with this specific label
# threshold: the number of professors you want to return

# return: a dataframe with sorted professor
def find_prof(path, label_1, threshold=3):
    #     label_score = pd.read_csv('label_score.csv').drop(columns=['Unnamed: 0','label_list'])
    label_score = pd.read_csv(path).drop(columns=['Unnamed: 0', 'label_list'])
    label_score = label_score.astype({"idx1": int, "idx2": int, "idx3": int})
    label_score = label_score.sort_values(by=['idx1', 'score1'], ascending=False)
    result = label_score.loc[label_score['idx1'] == label_1]
    return result[0:threshold]


# path: csv file path ('label_score.csv')
# label_1: the first label for the professor
# label_2: the second label for the professor

# return: one professor specialist on two fields
def find_expert(path, label_1, label_2):
    label_score = pd.read_csv(path).drop(columns=['Unnamed: 0', 'label_list'])
    label_score = label_score.astype({"idx1": int, "idx2": int, "idx3": int})
    label_score = label_score.sort_values(by=['idx1', 'score1'], ascending=False)
    result = label_score.loc[(label_score['idx1'] == label_1) & (label_score['idx2'] == label_2)]
    index = []
    for i in range(result.shape[0]):
        index.append(np.abs(result.iloc[i].score1 - result.iloc[i].score2))
    return result.iloc[np.argmin(index)]


if __name__ == '__main__':
    print('Find professor.')
