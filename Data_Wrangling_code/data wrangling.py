# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 13:30:42 2021

@author: guoqi
"""
import os
import pandas as pd
import numpy as np
import pickle

path = "C:/Users/guoqi/Desktop/nlp_project/April" # path to data 


#data = pd.DataFrame()
#for root, dirs, files in os.walk(path):
#    try:
#        for word in files:
#            label = word.split(' ')[0]
#            t_path = root + '/' + word
#            f = pd.read_csv(t_path)
#            d = pd.DataFrame({'user_id':f.user_id, 'text':f.text,
#                             'country':f.country_code, 'language':f.lang,
#                             'date':np.repeat(label,len(f))})
#            data = data.append(d)            
#    except Exception as e:
#        print (e)

#pickle.dump(data, open(path+"tweets.pkl", "wb"))

my_data = pickle.load(open(path+"tweets.pkl", "rb"))
        
update_data = my_data[(my_data['language'] == 'en') & (my_data['country'] == 'US')]


# getting sentiment scores
# 1) Simple sentiment score using negative words and positive words from HW3
path_words = "C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Data_Wrangling_code/words" #path to negative and positive words
words = pd.DataFrame()
for root, dirs, files in os.walk(path_words):
    try:
        for word in files:
            label = word.split('-')[0]
            t_path = root + '/' + word
            f = open(t_path,"r",encoding = 'latin-1')
            test_text = f.read().lower()
            test_text = test_text.split()
            f.close()
            words =  words.append(
                    {"label": label,
                     "body": test_text}, ignore_index=True)
    except Exception as e:
        print (e)
        pass    
pos_dict = words[words.label == 'positive'].body.iloc[0,]
neg_dict = words[words.label == 'negative'].body.iloc[0,]

def gen_senti(text_in):
    import re
    clean_text = re.sub('[^a-zA-Z]+', " ", text_in).lower().split()  
    pw = []
    nw = []
    for token in clean_text:
        if token in neg_dict:
            nw.append(token)
        elif token in pos_dict:
            pw.append(token)

    if(len(pw)+len(nw))==0:
        score = 0
    else:
        score = (len(pw)-len(nw))/(len(pw)+len(nw))
    return score

update_data['simple_senti'] = update_data.text.apply(gen_senti)

# 2) Vader Sentiment Score
def vader_senti(text_in):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    senti = SentimentIntensityAnalyzer()
    score = senti.polarity_scores(text_in)
    return score['compound']

update_data['vader_senti'] = update_data.text.apply(vader_senti)

#pickle.dump(update_data, open("C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Data_Wrangling_code/US_Eng_tweets_with_senti.pkl", "wb"))

update_data = pickle.load(open("C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Data_Wrangling_code/US_Eng_tweets_with_senti.pkl", "rb"))


