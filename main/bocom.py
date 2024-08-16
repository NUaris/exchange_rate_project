# -*- coding: utf-8 -*-
# @Time    : 2024/8/13 16:09
# @Author  : Nuaris

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time

chrome_options = Options()
chrome_options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
chrome_options.add_argument("--headless")  # 无界面模式
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


urls = {
    'boc': 'https://www.boc.cn/sourcedb/whpj/', #中国银行
    'hsbc': 'https://www.services.cn-banking.hsbc.com.cn/PublicContent/common/rate/zh/exchange-rates.html', #汇丰银行
    'icbc': 'https://icbc.com.cn/column/1438058341489590354.html', #中国工行
    'abc': 'https://ewealth.abchina.com/ForeignExchange/', #中国农业银行
    'bocom': 'https://www.bankcomm.com/BankCommSite/zonghang/cn/newWhpj/foreignExchangeSearch_Cn.html', #中国交通银行
    'ccb': 'https://forex2.ccb.com/chn/forex/exchange-quotations.shtml' #中国建设银行
}

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(urls['bocom'])
#driver.get('https://www.bankcomm.com/BankCommSite/zonghang/cn/newWhpj/foreignExchangeSearch_Cn.html')
time.sleep(5)
#WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//div[@class='cell' and text()='澳大利亚元(AUD/CNY)']")))
content = driver.page_source

#print(content)
if content:
    soup = BeautifulSoup(content, 'html.parser')
#print(soup)

 
# soup = BeautifulSoup(html_content, 'html.parser')
# 查找所有表格
# if soup:
#     tables = soup.find_all('table')
# else:
#     print("fail to load contents")
#     exit()
# for i in range(len(tables)):
#     print(i)
#     print(tables[i])
#     print("--------------------------")



# print(len(tables))

# # 确认是否找到至少三个表格
# # if len(tables) < 3:
# #     print("Failed to find the third table.")
# #     driver.quit()
# #     exit()


third_table = soup.find('table')
#print(third_table)
# # 获取表格中的所有行
#print("------------------------------------------------")
rows = third_table.find_all('tr')
#print(rows)

# 查找澳元 (AUD) 的行
aud_row = None
for row in rows:
    cells = row.find_all('td')
    if cells and "澳大利亚元(AUD/CNY)" in cells[0].get_text():
        aud_row = row


#print(aud_row)
cells = aud_row.find_all('td')

data = [cell.get_text(strip=True) for cell in cells]
# print(data)
# # 获取澳元的现汇卖出价
# aud_exchange_rate = None
# if aud_row:
#     cells = aud_row.find_all('td')
#     aud_exchange_rate = cells[3].get_text().strip() if len(cells) > 3 else "未找到现汇卖出价"

# last_time = datetime.now()
aud_exchange_rate = data[3]
last_time = datetime.now()

if aud_exchange_rate and last_time:
    print("中国交通银行")
    print(f"澳元现汇卖出价: {aud_exchange_rate}")
    print(f"{last_time}")
else:
    print("Failed to find the Australian Dollar row or the expected data.")

driver.quit()
