import requests
import pandas as pd
from bs4 import BeautifulSoup


# 请求URL
url = 'http://car.bitauto.com/xuanchegongju/?l=8&mid=8'
# 得到页面的内容
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
html = requests.get(url,headers=headers,timeout=10)
content = html.text
# 通过content创建BeautifulSoup对象
soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')

# 找到完整的价格搜索结果
price_table = soup.find('div', class_="search-result-list")
# 创建DataFrame
columns = ['名称', '最低价格', '最高价格', '图片链接']
df = pd.DataFrame(columns=columns)
tr_list = price_table.find_all('div', class_='search-result-list-item')

for tr in tr_list:
    img_path = tr.find('img')['src'] # 提取图片链接

    car_model_name = tr.find('p', class_="cx-name text-hover").string # 提取车型名称

    # 提取价格范围
    price_range = tr.find('p', class_="cx-price").string 
    if price_range == '暂无':
      cheapest_price = -1
      highest_price = -1
    else:
      cheapest_price = float(price_range.split('-')[0])
      highest_price = float(price_range.split('-')[1][:-1])

    new_row = {'名称': car_model_name, '最低价格': cheapest_price, 
                '最高价格': highest_price, '图片链接': img_path}
    df = df.append(new_row, ignore_index=True)

# 保存数据
df.to_csv('./exam/ProjectA/car_price.csv', index=False, encoding='utf-8-sig')

