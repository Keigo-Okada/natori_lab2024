関西大学総合情報学部名取ゼミ用コード

# analysisフォルダー
このフォルダー内では分析用コードと分析用データが格納されている。

## dataフォルダ
この中には分析用コードを用いる際に使用するデータを格納している。データは滋賀県草津市の2011年の議会内発言データを格納している。

## LDA
lda分析は、lda.pyとstopwords_list.txtを用いる。実際の分析はpythonで実行し、結果にノイズが多く生じる場合、ストップワードを設定し除去する。
Rを用いたlda.Rも存在する。こちらはquantedaを用いている。

詳しくはquantedaの公式サイトを参照。
[事例: 衆議院外務委員会の議事録](https://quanteda.io/articles/pkgdown/examples/japanese_speech_ja.html)

## tf-idf
市長と議員での発言内容にtf-idf分析を行う。

## クラスター分析
まずoutput_tf_matrix.pyを用いて、議員毎の行列を作成。その行列に対して、cluster.pyを用いて分析する。

# tool


