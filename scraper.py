from bs4 import BeautifulSoup
import requests
import time
import random
import pandas as pd  # 引入 pandas 用于保存 CSV

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

# 存储所有数据的列表
all_quotes = []

# 爬取指定页面
def scrape_quotes(start_page, end_page):
    for page in range(start_page, end_page + 1):
        url = f"http://quotes.toscrape.com/page/{page}/"
        print(f"正在爬取第 {page} 页: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")
            quotes = soup.find_all("div", class_="quote")
            if not quotes:
                print("没有找到更多名言，可能已到最后一页")
                break

            for quote in quotes:
                text = quote.find("span", class_="text").text.strip()
                author = quote.find("small", class_="author").text.strip()
                tags = [tag.text for tag in quote.find_all("a", class_="tag")]

                all_quotes.append({
                    "text": text,
                    "author": author,
                    "tags": ", ".join(tags)  # 将标签列表转换为字符串，用逗号分隔
                })

            print(f"第 {page} 页爬取完成，当前共收集 {len(all_quotes)} 条名言")

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            continue

        time.sleep(random.uniform(1, 3))

# 爬取第 1 到 3 页
scrape_quotes(1, 3)

# 保存到 CSV 文件
df = pd.DataFrame(all_quotes)
df.to_csv("quotes.csv", index=False)
print("数据已保存到 quotes.csv 文件")