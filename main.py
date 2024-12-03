import calendar
import re

import pandas as pd
import PySimpleGUI as sg


def get_days_in_month(year, month):
    # 指定された年月の月初めの日から月末までの日数を取得
    _, days_in_month = calendar.monthrange(year, month)

    # 日数のリストを生成
    days_list = list(range(1, days_in_month + 1))

    return days_list


def csv2xlsx(input_path, target_month, output_path):
    inp_data_gen = pd.read_csv(input_path)
    out_data = pd.DataFrame()
    out_data["名前"] = inp_data_gen["お名前"]
    target_year = 2024

    day_list = get_days_in_month(year=target_year, month=target_month)
    for day in day_list:
        out_data[day] = None
    # 最初[タイムスタンプ]と最後[連絡事項]を除外
    inp_data = inp_data_gen.iloc[:, 1:-1]
    check_day = check_table(inp_data)
    # 日ごとに処理
    for col in range(len(inp_data.columns[1:])):
        # 人ごとに処理
        for ind in range(len(inp_data.index)):
            if pd.isna(inp_data.loc[ind, col]):
                continue
            possible_times = re.split(",|:|;", inp_data.iloc[ind, col])
            alterd_time = replace_uni(possible_times)
            out_data.iloc[ind, col] = alterd_time
    out_data["連絡事項"] = inp_data_gen["連絡事項：コメント"]
    out_data.to_excel(output_path, index=False)
    sg.popup("完了しました！")


def check_table(ls: pd.DataFrame):
    day_sup = []
    # 日毎
    for col in range(len(ls.columns[1:])):
        # 人ごと
        for ind in range(len(ls.index)):
            day_sup.append(re.split(",|:|;", ls.loc[ind, col]))
    return day_sup  # [何日[いついつ]]


def replace_uni(a_list, check_day):
    time = ""
    for a in a_list:
        if int(a) == 1:
            time += "\u2460"
        elif int(a) == 2:
            time += "\u2461"
        elif int(a) == 3:
            time += "\u2462"
        elif int(a) == 4:
            time += "\u2463"
        else:
            time += " "
    return time


def extract_date(s):
    # 正規表現を使って数字を抽出
    match = re.search(r"\[(\d+)日\]", s)

    if match:
        extracted_number = int(match.group(1))
        return extracted_number


def main():
    sg.theme("DarkBlue3")
    layout = [
        [sg.Text("シフト作成アプリへようこそ！")],
        [sg.Text("シフト作成月を選択してください"), sg.InputText(key="-month-")],
        [sg.Text("出力先Excelファイル名:"), sg.InputText(key="-OUTPUT_FILE-")],
        [sg.Text("対象のCSVファイルを選択してください")],
        [sg.InputText(key="-FILE-", enable_events=True), sg.FileBrowse()],
        [sg.Button("アップロード"), sg.Button("終了")],
    ]

    window = sg.Window("Mywindow", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "終了"):
            break
        elif event == "アップロード":
            file_path = values["-FILE-"]
            target_month = int(values["-month-"])
            output_path = "~/Desktop/" + values["-OUTPUT_FILE-"] + ".xlsx"
            if file_path:
                csv2xlsx(file_path, target_month, output_path)
                window.close()

    window.close()


if __name__ == "__main__":
    main()


def get_days_in_month(year, month):
    # 指定された年月の月初めの日から月末までの日数を取得
    _, days_in_month = calendar.monthrange(year, month)

    # 日数のリストを生成
    days_list = list(range(1, days_in_month + 1))

    return days_list


def csv2xlsx(input_path, target_month, output_path):
    inp_data_gen = pd.read_csv(input_path)
    out_data = pd.DataFrame()
    out_data["名前"] = inp_data_gen["お名前"]
    target_year = 2024

    day_list = get_days_in_month(year=target_year, month=target_month)
    for day in day_list:
        out_data[day] = None
    # 最初[タイムスタンプ]と最後[連絡事項]を除外
    inp_data = inp_data_gen.iloc[:, 1:-1]
    # 日ごとに処理
    for col in range(len(inp_data.columns[1:])):
        # 人ごとに処理
        for ind in range(len(inp_data.index)):
            if pd.isna(inp_data.loc[ind, col]):
                continue
            possible_times = re.split(",|:|;", inp_data.iloc[ind, col])
            alterd_time = replace_uni(possible_times)
            out_data.iloc[ind, col] = alterd_time
    out_data["連絡事項"] = inp_data_gen["連絡事項：コメント"]
    out_data.to_excel(output_path, index=False)
    sg.popup("完了しました！")


def check_table(ls: pd.DataFrame):
    day_sup = []
    # 日毎
    for col in range(len(ls.columns[1:])):
        # 人ごと
        for ind in range(len(ls.index)):
            day_sup.append(re.split(",|:|;", ls.loc[ind, col]))
    return day_sup  # [何日[いついつ]]


def replace_uni(a_list, check_day):
    time = ""
    for a in a_list:
        if int(a) == 1:
            time += "\u2460"
        elif int(a) == 2:
            time += "\u2461"
        elif int(a) == 3:
            time += "\u2462"
        elif int(a) == 4:
            time += "\u2463"
        else:
            time += " "
    return time


def extract_date(s):
    # 正規表現を使って数字を抽出
    match = re.search(r"\[(\d+)日\]", s)

    if match:
        extracted_number = int(match.group(1))
        return extracted_number
