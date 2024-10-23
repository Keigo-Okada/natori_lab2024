library(tidyverse)

#定例会テーブルに記載している会議数と議事録の数がマッチするか判別するためのコード。

#最初8桁を日付として抽出する関数
extract_date <- function(file_name) {
    date_string <- gsub(".*/([0-9]{8}).*", "\\1", file_name)  # ファイル名から8桁の日付の部分を抽出
    date <- as.Date(date_string, format = "%Y%m%d")  # 日付型に変換
    return(date)
}

#フォルダー内のファイルをリスト型で取得する関数
list_files <- function(folder_path) {
    files <- list.files(folder_path, full.names = TRUE, recursive = TRUE)
    return(files)
}

#定例会テーブルの読み込み
df <- read_csv("/215.三木市/miki_teirei.csv")
 
#そのまま日付変換出来なかったため、一度分割した上で日付型として再度格納
# 年、月、日に分割して新しい列に保存
df$s_year <- substr(df$start_date, 1, 4)
df$s_month <- substr(df$start_date, 5, 6)
df$s_day <- substr(df$start_date, 7, 8)
df$f_year <- substr(df$final_date, 1, 4)
df$f_month <- substr(df$final_date, 5, 6)
df$f_day <- substr(df$final_date, 7, 8)

#年月日を繋げて日付型に変換
df$start_date <- as.Date(paste(df$s_year, df$s_month, df$s_day, sep = "-"))
df$final_date <- as.Date(paste(df$f_year, df$f_month, df$f_day, sep = "-"))

# 不要な列を削除
df <- df[, !(names(df) %in% c("s_year", "s_month", "s_day","f_year", "f_month", "f_day"))]

# フォルダー内のファイルの一覧を取得
folder_path <- "/28215.三木市/"
file_lists <- list_files(folder_path)
file_lists <- lapply(file_lists, extract_date)
#print(file_lists)

# カウント用の空のベクトルを作成
counts <- numeric(nrow(df))

#df内start_dateとfinal_dateの間にあるファイル数をカウントする
for (file_list in file_lists) {
    for (i in 1:nrow(df)) {
        if (file_list >= df$start_date[i] && file_list <= df$final_date[i]) {
            counts[i] <- counts[i] + 1
        }
    }
}
df$gijiroku_DL <- counts

#gijiroku_DL列の左隣の列と引き算し、過不足を確認
col_position <- which(names(df) == "gijiroku_DL")
result <- df %>% mutate(
    check = .[[col_position]] - .[[col_position - 1]]
)
view(result)

