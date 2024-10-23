library(tidyverse)

#議事録と定例会テーブルで擬似的会議テーブル作成
#定例会IDと会議IDの対応用コード


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
rmtg_df <- read_csv("/Users/okadakeigo/Downloads/215.三木市/miki_teirei.csv")
#そのまま日付変換出来なかったため、一度分割した上で日付型として再度格納
# 年、月、日に分割して新しい列に保存
rmtg_df$s_year <- substr(rmtg_df$start_date, 1, 4)
rmtg_df$s_month <- substr(rmtg_df$start_date, 5, 6)
rmtg_df$s_day <- substr(rmtg_df$start_date, 7, 8)
rmtg_df$f_year <- substr(rmtg_df$final_date, 1, 4)
rmtg_df$f_month <- substr(rmtg_df$final_date, 5, 6)
rmtg_df$f_day <- substr(rmtg_df$final_date, 7, 8)

#年月日を繋げて日付型に変換
rmtg_df$start_date <- as.Date(paste(rmtg_df$s_year,rmtg_df$s_month,rmtg_df$s_day, sep = "-"))
rmtg_df$final_date <- as.Date(paste(rmtg_df$f_year,rmtg_df$f_month,rmtg_df$f_day, sep = "-"))

# 不要な列を削除
rmtg_df <- rmtg_df[, names(rmtg_df) %in% c('ID_teirei', 'jis_code','start_date','final_date')]

# フォルダー内のファイルの一覧を取得
folder_path <- "/Users/okadakeigo/Downloads/28215.三木市/"
file_lists <- list_files(folder_path)
file_lists <- lapply(file_lists, extract_date)

#出力用の空のデータフレームを作成しておく
kaigi_df <- tibble(
    ID_teirei = character(),
    kaigi_id = character(),
    jis_code = character()
)

for (file_list in file_lists) {
    for (i in 1:nrow(rmtg_df)) {
        if (file_list >= rmtg_df$start_date[i] && file_list <= rmtg_df$final_date[i]){
            #要素を新たなデータフレームに追加し、それを結合する。
            append_row <- data.frame(ID_teirei = rmtg_df$ID_teirei[i], 
                                     kaigi_id = file_list,
                                     jis_code = rmtg_df$jis_code[i])
            kaigi_df <- rbind(kaigi_df, append_row)
        }
    }
}

#日付型から文字列に変更
kaigi_df$kaigi_id <- format(kaigi_df$kaigi_id, "%Y%m%d")
kaigi_df$kaigi_id <- paste(kaigi_df$kaigi_id, kaigi_df$jis_code, sep = "")

#各定例会に何回の会議があるかをカウント
count <- kaigi_df %>%
    group_by(ID_teirei) %>%
    summarize("会議数" = n())
#view(count)

#出力
write.csv(kaigi_df, "/Users/okadakeigo/Downloads/215.三木市/miki_kaigi.csv")
view(kaigi_df)


