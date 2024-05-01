import os
import re
import MeCab
import numpy as np
import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import copy
import gensim
import matplotlib.pyplot as plt
import japanize_matplotlib
import glob

#クラスター数の設定
n_cluster = 5

#ストップワードの設定
#stop_words = ['議員','市長','委員','宇治','三田','市','市民','部長','議案']
with open("/Users/keigookada/Desktop/seminar/code/LDA/stopwords_list.txt", "r", encoding="utf-8") as f:
    stop_words = f.readlines()
#print(type(stop_words))
#print(stop_words)
#stopwords内の改行文字"\n"を削除
newlinw_delete = "\n"
stop_words = [word.replace(newlinw_delete, "") for word in stop_words]
print(stop_words)

#ファイルのあるフォルダを指定
os.chdir('/Users/keigookada/Downloads/OneDrive_1_2024-1-15 (1)/奈良市3/')

#読み込んだcsvを格納するデータフレームの作成
hatsugen = pd.DataFrame(columns = [])

#ファイル内のcsvをデータフレームに格納
coltype = {'teirei_id': 'str','shicho_or_giin':'str'}
for i in glob.glob("*.csv"):
    tmp = pd.read_csv(i,dtype=coltype)
    hatsugen = pd.concat([hatsugen, tmp])


#発言内容の欠損の除去
hatsugen = hatsugen.dropna(subset=['statement'])
#議員の発言のみを抽出
#hatsugen = hatsugen[hatsugen["shicho_or_giin"] == "0.0"]
#1.0=市長,0.0=議員

#単一のcsvを使用する際に使う
#hatsugen = pd.read_csv("/Users/keigookada/Desktop/seminar/宇治市発言テーブル.csv")
#print(type(hatsugen))
#hatsugen["statement"] = hatsugen["statement"].str.replace(stop_words,'')

def parse(tweet_temp):
    t = MeCab.Tagger()
    temp1 = t.parse(tweet_temp)
    temp2 = temp1.split("\n")
    t_list = []
    for keitaiso in temp2:
        if keitaiso not in ["EOS",""]:
            word,hinshi = keitaiso.split("\t")
            t_temp = [word]+hinshi.split(",")
            if len(t_temp) != 10:
                t_temp += ["*"]*(10 - len(t_temp))
            t_list.append(t_temp)

    return t_list

def parse_to_df(tweet_temp):
    return pd.DataFrame(parse(tweet_temp),
                        columns=["単語","品詞","品詞細分類1",
                                 "品詞細分類2","品詞細分類3",
                                 "活用型","活用形","原形","読み","発音"])

def make_lda_docs(texts):
    docs = []
    for text in texts:
        df = parse_to_df(text)
        #print(type(df))
        extract_df = df[(df["品詞"]+"/"+df["品詞細分類1"]).isin(["名詞/一般","名詞/固有名詞"])]
        extract_df = extract_df[extract_df["原形"]!="*"]
        #print(type(extract_df))
        #extract_df.to_csv('/Users/keigookada/Desktop/seminar/形態素.csv')
        #extract_df[extract_df['単語'] != '市長']
        doc = []
        for genkei in extract_df["原形"]:
            doc.append(genkei)
        docs.append(doc)
    return docs

texts = hatsugen["statement"].values
#print(texts)
docs = make_lda_docs(texts)
#print(docs)
#print(type(docs))#リスト

docs = [[word for word in sublist if word not in stop_words] for sublist in docs]

dictionary = gensim.corpora.Dictionary(docs)
corpus = [dictionary.doc2bow(doc) for doc in docs]
#print(type(corpus))
#print(corpus)
#print(type(corpus))

lda = gensim.models.LdaModel(
                corpus=corpus,
                id2word=dictionary,
                num_topics=n_cluster, 
                minimum_probability=0.001,
                passes=20, 
                update_every=0, 
                chunksize=10000,
                random_state=1
                )

lists = []
for i in range(n_cluster):
    temp_df = pd.DataFrame(lda.show_topic(i),columns=["word","score"])
    temp_df["topic"] = i
    lists.append(temp_df)
topic_word_df = pd.concat(lists,ignore_index=True)

topic_word_df["rank"] = topic_word_df.groupby("topic")["score"].rank()
tocsv = topic_word_df.pivot(index='topic', columns='rank', values='word')

tocsv.to_csv('/Users/keigookada/Downloads/OneDrive_1_2024-1-15 (1)/奈良市2/奈良市3LDA結果5.csv',encoding="cp932")
