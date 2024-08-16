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

driver.get(urls['ccb'])
#WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//div[@class='cell' and text()='澳大利亚元(AUD)']")))
content = driver.page_source

#print(content)
if content:
    soup = BeautifulSoup(content, 'html.parser')
#print(soup)

 
# soup = BeautifulSoup(html_content, 'html.parser')
# 查找所有表格
if soup:
    lists = soup.find_all('ul')
# else:
#     print("fail to load contents")
#     exit()
# # for i in range(len(tables)):
# #     print(i)
# #     print(tables[i])
# #     print("--------------------------")



# # 查找澳元 (AUD) 的行
# aud_row = None
# for row in lists:
#     if row and "澳大利亚元" in row[0].get_text():
#         aud_row = row

for target_list in lists:
    items = target_list.find_all('li')
    for item in items:
        if item and "澳大利亚元" == item.get_text():
            aud_row = items
            break
data = []

# 从找到的行中提取数据
if aud_row:
    for item in aud_row:
        data.append(item.get_text().strip())
aud_exchange_rate = data[2]
last_time = data[5]

if aud_exchange_rate and last_time:
    print("中国建设银行")
    print(f"澳元现汇卖出价: {aud_exchange_rate}")
    print(f"{last_time}")
else:
    print("Failed to find the Australian Dollar row or the expected data.")

driver.quit()
