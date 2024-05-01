# 必要なパッケージのインストール
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import csv

#jis = "28219"
#city = "三田市"

# 分類するクラスタ数の設定
cls_n = 5

# 行に議員名、列に単語が記載されている行列データを読み込む
cls_df = pd.read_csv('/Users/keigookada/Downloads/kusatushi/草津市コーパス201509以降任期.csv')
#cls_df = pd.read_csv("../step1/大阪/copus_" + jis + city + ".csv", index_col=False)
# cls_df = pd.read_csv("../京都/26100/201102222610005平成23年2月定例会（第2回）−02月22日−01号.csv", index_col=False)

# 列に記載されている単語を変数へ挿入
col = cls_df.columns[1:].tolist()

# クラスタ分析の結果を入れる箱の初期化
cls_arr = np.empty((0, len(cls_df[col[0]])))

# クラスタ分析ができるデータ形式にデータを成形 1
i = 0
while i < len(col):
    cls_arr = np.append(cls_arr, np.array([cls_df[col[i]].tolist()]), axis=0)
    i += 1

# さらにクラスタ分析ができる形式(転置)へ成形 2
cls_arr = cls_arr.T

# クラスタ分析を実行し、変数predへ分類されたクラスタを挿入
pred = KMeans(n_clusters=cls_n).fit_predict(cls_arr)
# print(pred)
cls_df['cluster_id'] = pred


# 各クラスタに分類された議員の数を出力
# print (cls_df['cluster_id'].value_counts())

# クラスタごとに議員を出力
num = []
data = []
i = 0
while i <= cls_n:
    # print ("cluster", i)
    cls_name = "cluster " + str(i)
    print(cls_name)
    num.append(cls_name)

    # print (cls_df[cls_df['cluster_id']==i].iloc[:, 0])
    cls_data = cls_df[cls_df['cluster_id']==i].iloc[:, 0]
    print(cls_data)
    data.append(cls_data)

    i += 1

print(num)
print(data)

with open("/Users/keigookada/Downloads/kusatushi/草津市クラスター結果201509以降任期.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(num)
    writer.writerow(data)
