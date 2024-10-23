library(tidyverse)

#定例会IDに変更があるため、新旧IDをマッチングさせるためのコード。

df_t <- read_csv("/215.三木市/miki_teirei.csv")
df_i <- read_csv("/215.三木市/miki_iin.csv")

df_i$ID_teirei <- df_t$ID_teirei[match(df_i$旧ID, df_t$旧ID)]
write.csv(df_i,"/Users/okadakeigo/Downloads/215.三木市/miki_iinkai.csv")


