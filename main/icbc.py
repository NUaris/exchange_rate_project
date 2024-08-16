# -*- coding: utf-8 -*-
# @Time    : 2024/8/13 16:09
# @Author  : Nuaris
# @File    : icbc_test
# @Software: Vscode
# @Description: 中国工商银行外汇牌价爬取
# debuging: 1. 无法获取到数据，原因是网页加载速度过慢，导致数据未加载完成，解决方法：增加等待时间
# status: updating
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--headless")  # 无界面模式
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


urls = {
    'boc': 'https://www.boc.cn/sourcedb/whpj/', #中国银行
    'hsbc': 'https://www.services.cn-banking.hsbc.com.cn/PublicContent/common/rate/zh/exchange-rates.html', #汇丰银行
    'icbc': 'https://icbc.com.cn/column/1438058341489590354.html', #中国工行
    'abc': 'https://ewealth.abchina.com/ForeignExchange/', #中国农业银行
    'bocom': 'https://www.bankcomm.com/BankCommSite/shtml/jyjr/cn/7158/7161/8091/list.shtml', #中国交通银行
    'ccb': 'https://forex2.ccb.com/chn/forex/exchange-quotations.shtml' #中国建设银行
}

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(urls['icbc'])
WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//div[@class='cell' and text()='澳大利亚元(AUD)']")))
content = driver.page_source

#print(content)
if content:
    soup = BeautifulSoup(content, 'html.parser')
#print(soup)

 
# soup = BeautifulSoup(html_content, 'html.parser')
# 查找所有表格
if soup:
    tables = soup.find_all('table')
else:
    print("fail to load contents")
    exit()
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

# # 获取第三个表格
third_table = tables[2]
#print(third_table)
# # 获取表格中的所有行
rows = third_table.find_all('tr')


# 查找澳元 (AUD) 的行
aud_row = None
for row in rows:
    cells = row.find_all('td')
    if cells and "澳大利亚元(AUD)" in cells[0].get_text():
        aud_row = row



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
last_time = data[5]

if aud_exchange_rate and last_time:
    print("中国工商银行")
    print(f"澳元现汇卖出价: {aud_exchange_rate}")
    print(f"{last_time}")
else:
    print("Failed to find the Australian Dollar row or the expected data.")

driver.quit()
