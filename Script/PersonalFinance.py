# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 16:50:16 2021

@author: jinha
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import praw
import pandas as pd
import time
import datetime
import pytz
import os

#change dir
print(os.getcwd())
os.chdir('D:/GitHub/Datasets/Text')
print(os.getcwd())

#connect to reddit
reddit = praw.Reddit(client_id='4Ny8ZuJQqE_g4g',
                 client_secret="DPzsvF90jMWRBhjmgiFEfTrg9_RywA",
                 username='jjhasucis509',
                 password='zxcvbnm123',
                 user_agent='data_extract',
                 check_for_async=False)


#set a starting point of iterations
num = int(0)

#track the time
start = time.time()

#larger than 1 will lead to a periodical collecting
while num < 48:
    #update this iteration's info
    num += 1
    print("Round",num,"started at", datetime.datetime.now(pytz.timezone("America/Chicago")))
    start_i = time.time()
    
    #read ult-data
    df = pd.read_csv("PersonalFinance.csv")
    already_done = set(df.ID)
    df_len1 = len(df)
    
    #leagueoflegends - submission
    name = "personalfinance"
    s = reddit.subreddit(name)
    for i in s.comments(limit=None):
        if i.id not in already_done:
            q = str(i.id)
            w = i.author
            e = datetime.datetime.fromtimestamp(i.created_utc).strftime('%m/%d/%Y')
            r = i.score
            y = str(i.body).replace(";", "").replace("'","").replace(",","").replace("\"","").replace("\n", " ").replace("\r"," ")
            already_done.add(i.id)
            row = [q,w,e,r,y]
            a_series = pd.Series(row, index = df.columns)
            df = df.append(a_series, ignore_index=True)
            df.sort_values("Date", inplace=True)
            df.to_csv("PersonalFinance.csv",index=False)
            #print("Comments Loaded")
            
    #leagueoflegends - submission
    name = "personalfinance"
    s1 = reddit.subreddit(name)
    for i in s1.comments(limit=None):           
        i.refresh()
        i.replies.replace_more(limit=None)
        for comment in i.replies.list():
            if comment.id not in already_done:
                z = str(comment.id)
                x = comment.author
                c = datetime.datetime.fromtimestamp(comment.created_utc).strftime('%m/%d/%Y')
                v = comment.score
                n = str(comment.body).replace(";", "").replace("'","").replace(",","").replace("\"","").replace("\n", " ").replace("\r"," ")
                already_done.add(comment.id)
                row = [z,x,c,v,n]
                a_series = pd.Series(row, index = df.columns)
                df = df.append(a_series, ignore_index=True)
                df.sort_values("Date", inplace=True)
                df.to_csv("PersonalFinance.csv",index=False)
                #print("Replies Loaded")
                
                
    print("Number of Records in the Data:", len(df))
    print("Number of Unique ID:", len(df.ID.value_counts()))
    df_len2 = len(df)
    print("Number of Records Increased:", df_len2 - df_len1)
    
    

    #### conclud
    end_i = time.time()
    sec_i = end_i - start_i
    print("Round",num,"completed at", datetime.datetime.now(pytz.timezone("America/Chicago")))
    print("Time Lapses:",str(datetime.timedelta(seconds=sec_i)))
    print("\n")
    time.sleep(900)
    



end = time.time()
sec = end - start
str(datetime.timedelta(seconds=sec))





#print(datetime.datetime.now(pytz.timezone("America/Chicago")))