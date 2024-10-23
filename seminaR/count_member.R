library(tidyverse)
library(dplyr)

#定例会IDごとの議員数をチェックするためのコード。


df_m <- read_csv("/Users/okadakeigo/Downloads/215.三木市/miki_iinkai.csv")

# 特定の列が欠損値を含む行を削除
df_m <- df_m %>% filter(!is.na(ID_teirei))
#view(df_m)
#各定例会の参加人数
member_count <- df_m %>%
    group_by(ID_teirei) %>%
    summarize(議員数 = n())
view(member_count)

#名前と会派でグルーピングする
party_df <- df_m %>%
    group_by(name,kaiha) %>%
    summarize(所属会派での定例会参加数 = n())
view(party_df)

a <- df_m %>%
    group_by(ID_teirei,kaiha) %>%
    summarize(会派数 = n())
