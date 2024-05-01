#分析用コード
#コードの解説はRMDを参照

#パッケージの読み込み
library(quanteda)
library(stringr)
library(dplyr)
library(lubridate)
library(topicmodels)
library(tidyverse)

devtools::install_github("quanteda/quanteda.corpora")
full_corp <- quanteda.corpora::download("data_corpus_foreignaffairscommittee")
devtools::install_github("amatsuo/kaigiroku")

library(kaigiroku)

#データの読み込み
#df <- read_csv("/Users/keigookada/Desktop/seminar/code/hr_minutes/2011060925201_t.csv")
#df$row_id <- seq_len(nrow(df))

#複数の場合
#読み込みたいフォルダーを指定
file_list <- list.files("/Users/keigookada/Library/Mobile Documents/com~apple~CloudDocs/Keigo Okada/seminar/seminaR/nara2019/", pattern = ".csv", full.names = TRUE)
df <- readr::read_csv(file_list, id = "file_name")
df$row_id <- seq_len(nrow(df))

my_corpus <- corpus(df, text_field = "statement", docid_field = "row_id")

#トークン化
toks <- tokens(my_corpus)
toks <- tokens_select(toks, "^[０-９ぁ-んァ-ヶー一-龠]+$", valuetype = "regex", padding = TRUE)
toks <- tokens_remove(toks, c("御", "君"), padding = TRUE)

min_count <- 10

# 漢字
library("quanteda.textstats")
kanji_col <- tokens_select(toks, "^[一-龠]+$", valuetype = "regex", padding = TRUE) |> 
    textstat_collocations(min_count = min_count)
toks <- tokens_compound(toks, kanji_col[kanji_col$z > 3,], concatenator = "")

# カタカナ
kana_col <- tokens_select(toks, "^[ァ-ヶー]+$", valuetype = "regex", padding = TRUE) |> 
    textstat_collocations(min_count = min_count)
toks <- tokens_compound(toks, kana_col[kana_col$z > 3,], concatenator = "")

# 漢字，カタカナおよび数字
any_col <- tokens_select(toks, "^[０-９ァ-ヶー一-龠]+$", valuetype = "regex", padding = TRUE) |> 
    textstat_collocations(min_count = min_count)
toks <- tokens_compound(toks, any_col[any_col$z > 3,], concatenator = "")

speech_dfm <- dfm(toks) |>
    dfm_remove("") |> 
    dfm_remove("^[ぁ-ん]+$", valuetype = "regex", min_nchar = 2) |> 
    dfm_trim(min_termfreq = 0.50, termfreq_type = "quantile", max_termfreq = 0.99)

#分析

#ageの欠損値の除去
speech_dfm <- speech_dfm[complete.cases(docvars(speech_dfm, "age")), ]
#相対頻度分析
key <- textstat_keyness(speech_dfm, docvars(speech_dfm, "age") >= 50)
head(key, 20) |> knitr::kable()

#LDA
set.seed(100)
lda <- LDA(convert(speech_dfm, to = "topicmodels"), k = 10)
get_terms(lda, 10) |> knitr::kable()
