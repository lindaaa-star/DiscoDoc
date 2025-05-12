import tkinter as tk
from tkinter import messagebox
import pandas as pd

# 读取导师数据
def load_advisors():
    import os
    print("当前工作目录:", os.getcwd())
    file_path = "/Users/lindali/PhDAdvisorAPP/advisors.csv"
    print("文件是否存在:", os.path.exists(file_path))
    return pd.read_csv(file_path)

# 筛选导师
def filter_advisors(field, university, country):
    advisors = load_advisors()
    if field:
        advisors = advisors[advisors["Field"].str.contains(field, case=False, na=False)]
    if university:
        advisors = advisors[advisors["University"].str.contains(university, case=False, na=False)]
    if country:
        advisors = advisors[advisors["Country"].str.contains(country, case=False, na=False)]
    return advisors

# 更新结果显示
def update_results():
    result_listbox.delete(0, tk.END)
    field = field_entry.get().strip()
    university = university_entry.get().strip()
    country = country_entry.get().strip()
    results = filter_advisors(field, university, country)
    if results.empty:
        messagebox.showinfo("结果", "没有找到符合条件的导师！")
    else:
        for _, row in results.iterrows():
            result_listbox.insert(tk.END, f"{row['Name']} - {row['Field']} - {row['University']} - {row['Country']}")

# 创建主窗口
root = tk.Tk()
root.title("博士生导师筛选器")
root.geometry("600x400")

# 输入框和标签
tk.Label(root, text="研究领域:").pack(pady=5)
field_entry = tk.Entry(root, width=50)
field_entry.pack()

tk.Label(root, text="大学:").pack(pady=5)
university_entry = tk.Entry(root, width=50)
university_entry.pack()

tk.Label(root, text="国家:").pack(pady=5)
country_entry = tk.Entry(root, width=50)
country_entry.pack()

# 筛选按钮
tk.Button(root, text="筛选导师", command=update_results).pack(pady=10)

# 结果显示框
result_listbox = tk.Listbox(root, width=80, height=10)
result_listbox.pack(pady=10)

# 启动主循环
root.mainloop()
