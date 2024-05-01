from calendar import month
import json
import os
import pandas as pd
import re
import csv
import MeCab
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from operator import itemgetter

mecab = MeCab.Tagger()
mecab.parseToNode("")

#month = "6"
#day = "21"

def append_statement(arg_name,arg_statement,arg_age,arg_gender,arg_kaiha,arg_month,arg_day):

    # 4/1から3/31までを1年度とするための処理
    #date = re.split('[-/]', arg_day)
    date = arg_month
    print(type(date))
    print(date)
    if re.search('01'or'02'or'03', date):
        date[0] = int(date[0]) - 1

    if int(date[0]) <= 2018:
        if arg_name in d:
            d[arg_name] += arg_statement
        else:
            d[arg_name] = arg_statement

# files = []
# path = "../../npo/kaiha/"
# for x in os.listdir(path):
#     if(x[-4:] == 'xlsx'):
#         if os.path.isfile(path + x):
#             files.append(x)

kaiha_info = {}
# for file in files:
#     print ("委員会", file)
#     df = pd.read_excel(path + file, index_col=False, dtype='object')
#     for i, r in df.iterrows():
#         if str(r[2]) not in kaiha_info:
#             kaiha_info[str(r[2])] = r.kaiha
#         else:
#             print ("else")

d = {}
files = []
path = "/Users/keigookada/Downloads/kusatushi/201509以降/"
for x in os.listdir(path):
    if(x[-4:] == '.csv'):
        if os.path.isfile(path + x):
            files.append(x)

# print(files)

#読み込むデータ型の指定
coltype = {'teirei_id':'str','kaigi_id':'str','shicho_or_giin': str}

for file in files:
    print (file)
    df = pd.read_csv(path + file, index_col=False,dtype = coltype)
    #,usecols=['speaker','statement','age','gender','kaiha','teirei_id','month','day']
    # 議員の発言のみをDataFrameへ代入する
    #df = df[df["status"] == "3.0"]
    #print(df)
    #print(df.info)
    #print(df.columns)
    #df = df.drop(columns=['','ID_kaigi', 'new_and_old','status','jis_code','year'], inplace=True)
    #会議IDから年月日の取得
    df['year'] = df['kaigi_id'].str[:4]
    df['month'] = df['kaigi_id'].str[5:6]
    df['day'] = df['kaigi_id'].str[7:8]

    df = df.dropna(subset=['day'])
    df = df.dropna(subset=['month'])
    df = df.dropna(subset=['statement'])

    #議員だけを抽出
    df = df[df['shicho_or_giin'] == '0.0']
    print(df['shicho_or_giin'])
    for index, row in df.iterrows():
        #if ('委員会' not in file) and ('協議会' not in file) and ('講演会' not in file) and ("定例" in file):
            #print ("定例会", file)
            if not isinstance(row.statement, float):# 空白行を処理対象から除外する処理
                # append_statement(row.会議の開催日, row.議員id, row.発言者, row.発言内容, "定例会")
                tmp = ""
                for ki, vi in kaiha_info.items():
                    if (row.giin_name) == str(ki):
                        tmp = vi
                        continue
                #print(row.giin_id, row.giin_name, row.statement, row.gender, row.age, row.party_name,row.date)
                name = row['speaker']
                statement = row['statement']
                kaigi_id = row['kaigi_id']
                teirei_id = row['teirei_id']
                age = row['age']
                gender = row['gender']
                kaiha = row['kaiha']
                month = row['month']
                day = row['day']




                append_statement(name,statement,age,gender,kaiha,month,day)
                print(type(append_statement))
"""
        elif ("臨時" in file):
            pass
            #print ("臨時会", file)
            #if not isinstance(row.statement, float):# 空白行を処理対象から除外する処理
            #    append_statement(row.date, row.giin_id, row[4], row.statement, "臨時会")
        else:
            pass
            #print ("委員会", file)
            #if not isinstance(row.statement, float):# 空白行を処理対象から除外する処理
            #    append_statement(row.date, row.giin_id, row[4], row.statement, "委員会")
"""
print(type(df))
copus = []
copus2 = []
member = []
for k, v in d.items():
    node = mecab.parseToNode(v)
    noun = []
    while node:
        if node.feature.startswith('名詞'):
            if (not node.feature.split(',')[1] == "数"):
                noun.append(node.surface)
        node = node.next
    copus.append([' '.join(map(str, noun))])
    member.append(k)
#print(copus)
#print(type(copus))
#print(copus2)
#print(member)

copus = [' '.join(d) for d in copus]
print(len(copus))
count_vectorizer = CountVectorizer()
count_vectorizer.fit(copus)
x = count_vectorizer.transform(copus)

c = zip(count_vectorizer.get_feature_names()[:], x.toarray()[0, :])
q = sorted(c, key=itemgetter(1))
top500 = q[-500:]
print (top500)

top500_term = []
for t in top500:
    top500_term.append(t[0])

copus = [d.split(' ') for d in copus]
i = 0
while i < len(copus):
    noun2 = []
    j = 0
    while j < len(copus[i]):
        if copus[i][j] in top500_term:
            noun2.append(copus[i][j])
        j += 1
    copus2.append(noun2)
    i += 1
print (len(copus2))
copus2 = [' '.join(d) for d in copus2]
count_vectorizer2 = CountVectorizer()
count_vectorizer2.fit(copus2)
x2 = count_vectorizer2.transform(copus2)
df = pd.DataFrame(x2.toarray(), columns=count_vectorizer2.get_feature_names(), index=member)
print(df)
df.to_csv("/Users/keigookada/Downloads/kusatushi/草津市コーパス201509以降任期.csv")
