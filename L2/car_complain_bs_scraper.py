import requests
import pandas as pd
from bs4 import BeautifulSoup


# 请求URL
url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-1.shtml'
# 得到页面的内容
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
html=requests.get(url,headers=headers,timeout=10)
content = html.text
# 通过content创建BeautifulSoup对象
soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')

# 找到完整的投诉信息框
complain_table = soup.find('div',class_="tslb_b")
# 创建DataFrame
columns = ['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status']
df = pd.DataFrame(columns=columns)
tr_list = complain_table.find_all('tr')

for tr in tr_list:
    # 提取汽车投诉信息
    row_content = tr.find_all('td')
    if 0 == len(row_content):
      # Do nothing if no td found
      continue
    # status is stored in 'em' other than 'td'
    row_content[7] = tr.find('em')
    new_row = {col_name:td.string for col_name, td in zip(columns, row_content)}
    df = df.append(new_row, ignore_index=True)

# use utf-8-sig for proper decoding in Excel
df.to_csv('./L2/car_complain.csv', index=False, encoding='utf-8-sig')

