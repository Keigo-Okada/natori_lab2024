library(tidyverse)
library(dplyr)

df <- read_csv("/Users/keigookada/Desktop/seminar/nagahama.csv")

# 特定の列が欠損値を含む行を削除
df <- df %>% filter(!is.na(定例会開始日))
view(df)
#各定例会の参加人数
member_count <- df %>%
  group_by(定例会開始日) %>%
  summarize(議員数 = n())
view(member_count)

#名前と会派でグルーピングする
party_df <- df %>%
  group_by(name,会派) %>%
  summarize(所属会派での定例会参加数 = n())
view(party_df)
