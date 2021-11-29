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
df = pd.read_csv("PersonalFinance.csv")
df_len1 = list()
sub_len1 = list()

#larger than 1 will lead to a periodical collecting
while True:
    
    #update this iteration's info
    num += 1
    print("Round",num,"started at", datetime.datetime.now(pytz.timezone("America/Chicago")))
    start_i = time.time()
    
    #read ult-data
    already_done1 = set(df.Submission_Id)
    already_done2 = set(df.Reply_Id)
    df_len1.append(len(df))
    sub_len1.append(len(df.Submission_Id.value_counts()))

    #leagueoflegends - submission
    name = "personalfinance"
    s = reddit.subreddit(name)
    for i in s.new(limit=None):
        if i.id not in already_done1:
            q = str(i.id)
            t = str(i.id)
            p = i.title
            w = i.author
            e = datetime.datetime.fromtimestamp(i.created_utc).strftime('%m/%d/%Y')
            r = i.score
            y = str(i.selftext).replace(";", "").replace("'","").replace(",","").replace("\"","").replace("\n", " ").replace("\r"," ")
            already_done1.add(i.id)
            row = [q,t,p,w,e,r,y]
            a_series = pd.Series(row, index = df.columns)
            df = df.append(a_series, ignore_index=True)
            df.sort_values("Date", inplace=True)
            df.to_csv("PersonalFinance.csv",index=False)
            #print("Comments Loaded")

            for comment in i.comments:
                if comment.id not in already_done2:
                    b = str(i.id)
                    z = str(comment.id)
                    m = i.title
                    x = comment.author
                    c = datetime.datetime.fromtimestamp(comment.created_utc).strftime('%m/%d/%Y')
                    v = comment.score
                    n = str(comment.body).replace(";", "").replace("'","").replace(",","").replace("\"","").replace("\n", " ").replace("\r"," ")
                    already_done2.add(comment.id)
                    row = [b,z,m,x,c,v,n]
                    a_series = pd.Series(row, index = df.columns)
                    df = df.append(a_series, ignore_index=True)
                    df.sort_values(["Submission_Id", "Date"], ascending = (False, False), inplace=True)
                    df.to_csv("PersonalFinance.csv",index=False)
                    #print("Replies Loaded")
                    
            i.comments.replace_more(limit=None)
            for comment in i.comments.list():
                if comment.id not in already_done2:
                    b = str(i.id)
                    z = str(comment.id)
                    m = i.title
                    x = comment.author
                    c = datetime.datetime.fromtimestamp(comment.created_utc).strftime('%m/%d/%Y')
                    v = comment.score
                    n = str(comment.body).replace(";", "").replace("'","").replace(",","").replace("\"","").replace("\n", " ").replace("\r"," ")
                    already_done2.add(comment.id)
                    row = [b,z,m,x,c,v,n]
                    a_series = pd.Series(row, index = df.columns)
                    df = df.append(a_series, ignore_index=True)
                    df.sort_values(["Submission_Id", "Date"], ascending = (False, False), inplace=True)
                    df.to_csv("PersonalFinance.csv",index=False)
                    #print("Replies Loaded")
            
                
    print("Number of Records in the Data:", len(df))
    print("Number of Unique Replies:", len(df.Reply_Id.value_counts()))
    print("Number of Submissions:", len(df.Submission_Id.value_counts()))
    sub_len2 = len(df.Submission_Id.value_counts())
    print("Number of Submissions Increased:", sub_len2 - sub_len1[-1])
    df_len2 = len(df)
    print("Number of Records Increased:", df_len2 - df_len1[-1])
    
    #### conclud
    end_i = time.time()
    sec_i = end_i - start_i
    print("Round",num,"completed at", datetime.datetime.now(pytz.timezone("America/Chicago")))
    print("Time Lapses:",str(datetime.timedelta(seconds=sec_i)))
    print("\n")
    time.sleep(1800)