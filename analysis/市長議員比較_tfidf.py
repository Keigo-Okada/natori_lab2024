# coding: utf-8
import os
import re
import MeCab
import numpy as np
import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import copy

word = ""
words = []
stop_words = ["僕", "部", "課", "だれ", "すべて", "室"]

def tfidf(x):
    global tfidf_x
    global index
    global feature_words

    vectorizer = TfidfVectorizer(token_pattern='(?u)\\b\\w+\\b', min_df=1, max_df=0.5, max_features=2000)
    tfidf_x = vectorizer.fit_transform(x).toarray()
    index = tfidf_x.argsort(axis=1)[:,::-1]
    feature_names = np.array(vectorizer.get_feature_names_out())
    feature_words = feature_names[index]

def wakati(x):
    global word
    global docs
    global words

    mecab = MeCab.Tagger()
    mecab.parseToNode("")
    node = mecab.parseToNode(x)
    while node:
        if node.feature.startswith('名詞'):
            if (not node.surface in stop_words):
                if (not node.feature.split(',')[1] == "数"):
                    word += node.surface
        else:
            if word is not "":
                words.append(word)
                word = ""
        node = node.next

docs = []
docs_x1 = []
docs_x2 = []
files = []
path = "/Users/keigookada/Downloads/25209_甲賀市/2017/"
#カラム形式の設定
coltype = {'teirei_id':'str','kaigi_id':'str','shicho_or_giin': str}

for x in os.listdir(path):
    if(x[-4:] == '.csv') and ('委員会' not in x):
        if os.path.isfile(path + x):
            files.append(x)

d = {}
other_files = []
for file in files:
    year = file[:4]
    if "定例会" or "通常会議" in file:
        if file[4:6] == "02" or file[4:6] == "03":
            if year + "03" not in d:
                d[year + "03"] = pd.read_csv(path + file, index_col=False, dtype='object')
            else:
                df = pd.read_csv(path + file, index_col=False, dtype='object')
                d[year + "03"] = pd.concat([d[year + "03"], df])
        elif file[4:6] == "06" or file[4:6] == "05":
            if year + "06" not in d:
                d[year + "06"] = pd.read_csv(path + file, index_col=False, dtype='object')
            else:
                df = pd.read_csv(path + file, index_col=False, dtype='object')
                d[year + "06"] = pd.concat([d[year + "06"], df])
        elif file[4:6] == "09" or file[4:6] == "10" or file[4:6] == "08":
            if year + "09" not in d:
                d[year + "09"] = pd.read_csv(path + file, index_col=False, dtype='object')
            else:
                df = pd.read_csv(path + file, index_col=False, dtype='object')
                d[year + "09"] = pd.concat([d[year + "09"], df])
        elif file[4:6] == "01" or file[4:6] == "12" or file[4:6] == "11":
            if year + "12" not in d:
                d[year + "12"] = pd.read_csv(path + file, index_col=False, dtype='object')
            else:
                df = pd.read_csv(path + file, index_col=False, dtype='object')
                d[year + "12"] = pd.concat([d[year + "12"], df])
        else:
            print ("その他")
            print (file)
            other_files.append(file)

print (len(d))
print (type(d))
print (d.keys())
main = []
for k, v in sorted(d.items()):
    main.append(k)
    print (v['shicho_or_giin'])
    x0 = v[(v['shicho_or_giin'] == "1.0") | (v['shicho_or_giin'] == "0.0")]
    x1 = x0[x0['shicho_or_giin'] == "1.0"]
    x2 = x0[x0['shicho_or_giin'] == "0.0"]
    #status = 市長:1,議長:2,議員:3,その他:4
    print (len(x0))
    print (len(x1))
    print (len(x2))
    print ("")

    targetMecab = [x0, x1, x2]
    print (x0)
#上記のカッコでエラーが出たため変更
    i = 0
    while i < len(targetMecab):
        word = ""
        doc = []
        words = []

        for line in targetMecab[i].statement:
            if not isinstance(line, float):
                line = re.sub('¥s|　|¥n|¥r', '', line)
                wakati(line)

        doc.append(words)
        doc = [' '.join(d) for d in doc]

        if i == 0:
            docs.append(doc)
        elif i == 1:
            docs_x1.append(doc)
        else:
            docs_x2.append(doc)
        i += 1

docs = [' '.join(d) for d in docs]
docs_x1 = [' '.join(d) for d in docs_x1]
docs_x2 = [' '.join(d) for d in docs_x2]
docs_list = [docs, docs_x1, docs_x2]

i = 0
while i < len(main):
    score_tfidf = []
    score_tfidf_x1 = []
    score_tfidf_x2 = []
    feature_words_flatten = []
    feature_words_flatten_x1 = []
    feature_words_flatten_x2 = []

    j = 0
    while j < len(docs_list):
        docs_tmp = copy.copy(docs)
        docs_tmp[i] = copy.copy(docs_list[j][i])

        tfidf(docs_tmp)
        if j == 0:
            score_tfidf.append(tfidf_x[i][index[i]][:10])
            feature_words_flatten.append(feature_words[i][:10])
        elif j == 1:
            score_tfidf_x1.append(tfidf_x[i][index[i]][:10])
            feature_words_flatten_x1.append(feature_words[i][:10])
        else:
            score_tfidf_x2.append(tfidf_x[i][index[i]][:10])
            feature_words_flatten_x2.append(feature_words[i][:10])

        j += 1
    i += 1

    for term, idf, term_x1, idf_x1, term_x2, idf_x2 in zip(feature_words_flatten, score_tfidf, feature_words_flatten_x1, score_tfidf_x1, feature_words_flatten_x2, score_tfidf_x2):
        # f = open("/Users/keigookada/Dropbox ("/Users/keigookada/Downloads/卒論/tf-idf/男女別結果/滋賀県/大津市_男女別tf-idf.csv" + main[i-1] + ".csv", "w")
        with open("/Users/keigookada/Downloads/25209_甲賀市/甲賀市2017_市長議員別tf-idf.csv", "a") as f:
            writer = csv.writer(f, lineterminator='\n')

            writer.writerow([main[i-1]])
            writer.writerow(['市長議員', '', '市長', '', '議員'])

            for t, id, t_x1, i_x1, t_x2, i_x2 in zip(term, idf, term_x1, idf_x1, term_x2, idf_x2):
                csvlist = []
                csvlist.append(t)
                csvlist.append(id)
                csvlist.append(t_x1)
                csvlist.append(i_x1)
                csvlist.append(t_x2)
                csvlist.append(i_x2)
                writer.writerow(csvlist)
            f.close()
print("finish")