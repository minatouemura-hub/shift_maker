import calendar
import re
import tkinter as tk
import traceback
from datetime import datetime
from tkinter import filedialog, messagebox

import chardet  # エンコーディング自動検出用
import pandas as pd
from charset_normalizer import detect as charset_detect


def detect_encoding(file_path):
    """ファイルのエンコーディングを検出"""
    with open(file_path, "rb") as f:
        raw_data = f.read()
        # charset_normalizer を優先
        result = charset_detect(raw_data)
        if result["confidence"] >= 0.8:  # 信頼度が高い場合
            return result["encoding"]
        # 信頼度が低い場合は chardet にフォールバック
        result = chardet.detect(raw_data)
        return result["encoding"]


def get_days_in_month(year, month):
    """指定された年月の日数を取得"""
    _, days_in_month = calendar.monthrange(year, month)
    return list(range(1, days_in_month + 1))


def csv2xlsx(input_path, target_month, output_path):
    if ".xlsx" not in output_path:
        output_path = output_path + ".xlsx"
    try:
        try:
            # 入力ファイルのエンコーディングを検出して読み込む
            encoding = detect_encoding(input_path)
            inp_data_gen = pd.read_csv(input_path, encoding=encoding)
        except UnicodeDecodeError:
            input_path = pd.read_csv(input_path, encoding="shift_jis")

        out_data = pd.DataFrame()
        out_data["名前"] = inp_data_gen["お名前"]
        target_year = datetime.now().year

        day_list = get_days_in_month(year=target_year, month=target_month)
        for day in day_list:
            out_data[day] = None

        # 最初[タイムスタンプ]と最後[連絡事項]を除外
        inp_data = inp_data_gen.iloc[:, 1:-1]  # 0列目には名前

        # 日ごとに処理
        for col in range(1, len(inp_data.columns[1:]), 1):
            for ind in range(len(inp_data.index)):
                if pd.isna(inp_data.iloc[ind, col]):
                    continue
                possible_times = re.split(",|:|;", inp_data.iloc[ind, col])
                alterd_time = replace_uni(possible_times)
                out_data.iloc[ind, col] = alterd_time

        out_data["連絡事項"] = inp_data_gen["連絡事項：コメント"]
        out_data.to_excel(output_path, index=False)
        messagebox.showinfo("完了", "処理が完了しました！")
    except Exception as e:  # noqa
        error_details = traceback.format_exc()  # 詳細なエラーメッセージを取得
        messagebox.showerror("エラー", f"エラーが発生しました:\n{error_details}")


def replace_uni(a_list):
    """数値を丸囲み文字に変換"""
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


def main():
    def select_file():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

    def save_file():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")]
        )
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

    def process():
        file_path = file_entry.get()
        output_path = output_entry.get()
        try:
            target_month = int(month_entry.get())
            if file_path and output_path:
                csv2xlsx(str(file_path), target_month, str(output_path))
        except ValueError:
            messagebox.showerror("エラー", "月は数字で入力してください！")

    # GUI作成
    root = tk.Tk()
    root.title("シフト作成アプリ")

    tk.Label(root, text="シフト作成アプリへようこそ！").grid(row=0, column=0, columnspan=3, pady=10)

    tk.Label(root, text="シフト作成月:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    month_entry = tk.Entry(root)
    month_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="CSVファイルを選択:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    file_entry = tk.Entry(root, width=40)
    file_entry.grid(row=2, column=1, padx=5, pady=5)
    tk.Button(root, text="参照", command=select_file).grid(row=2, column=2, padx=5, pady=5)

    tk.Label(root, text="出力ファイル名:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    output_entry = tk.Entry(root, width=40)
    output_entry.grid(row=3, column=1, padx=5, pady=5)
    tk.Button(root, text="参照", command=save_file).grid(row=3, column=2, padx=5, pady=5)

    tk.Button(root, text="実行", command=process).grid(row=4, column=1, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
