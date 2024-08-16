# -*- coding: utf-8 -*-
# @Time    : 2024/8/13 16:09
# @Author  : Nuaris
# @status  : updating
import requests
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

#setting up the chrome options
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--headless")  # 无界面模式
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

#urls for the different banks
urls = {
    'boc': 'https://www.boc.cn/sourcedb/whpj/', #中国银行
    'hsbc': 'https://www.services.cn-banking.hsbc.com.cn/PublicContent/common/rate/zh/exchange-rates.html', #汇丰银行
    'icbc': 'https://icbc.com.cn/column/1438058341489590354.html', #中国工行
    'abc': 'https://ewealth.abchina.com/ForeignExchange/', #中国农业银行
    'bocom': 'https://www.bankcomm.com/BankCommSite/zonghang/cn/newWhpj/foreignExchangeSearch_Cn.html', #中国交通银行
    'ccb': 'https://forex2.ccb.com/chn/forex/exchange-quotations.shtml' #中国建设银行
}

#main code

#boc
def search_boc():
    # 中国银行
    # 初始化变量
    bank_name = "中国银行"
    aud_exchange_rate = None
    update_time = None
    # 获取中国银行汇率页面内容
    response = requests.get(urls['boc'])
    response.encoding = 'utf-8'  # 设置正确的编码

    # 检查请求是否成功
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return bank_name,False,response.status_code

    # 解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有表格
    tables = soup.find_all('table')

    # 确认是否找到至少两个表格
    if len(tables) < 2:
        print("Failed to find the second table.")
        return bank_name,False,'Failed to find the second table.'

    # 获取第二个表格
    second_table = tables[1]
    # 获取表格中的所有行
    rows = second_table.find_all('tr')

    # 查找澳大利亚元的汇率行
    for row in rows:
        cells = row.find_all('td')
        if cells and cells[0].get_text().strip() == "澳大利亚元":
            aud_exchange_rate = cells[3].get_text().strip()  # 第三个数据
            update_time = cells[-2].get_text().strip()   # 倒数第二个数据
            break
    
    if aud_exchange_rate and update_time:
        return bank_name, aud_exchange_rate, update_time  
    else:
        return bank_name, False, 'NO AUD data found'

#hsbc
def search_hsbc():
    # 汇丰银行
    # 初始化变量
    bank_name = "汇丰银行"
    aud_exchange_rate = None
    update_time = None
    # 使用 WebDriver Manager 自动管理 ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(urls['hsbc'])
    # 等待页面加载
    time.sleep(5)
    # 获取页面内容
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # 查找所有表格
    tables = soup.find_all('table')
 
    # 获取第三个表格
    third_table = tables[2]
    # 获取表格中的所有行
    rows = third_table.find_all('tr')

    # 查找最后更新时间
    last_time_tag = None
    for row in rows:
        last_time_tag = row.find('td', class_='ForTime01')
        if last_time_tag:
            break
    update_time = last_time_tag.get_text().strip() if last_time_tag else "unable to find the last update time"

    # 查找澳元 (AUD) 的行
    aud_row = None
    for row in rows:
        cells = row.find_all('td')
        if cells and "澳元 (AUD)" in cells[0].get_text():
            aud_row = row
            break

    # 获取澳元的现汇卖出价
    if aud_row:
        cells = aud_row.find_all('td')
        aud_exchange_rate = cells[2].get_text().strip() if len(cells) > 3 else "未找到现汇卖出价"

    driver.quit()


    if aud_exchange_rate and update_time:
        return bank_name, aud_exchange_rate, update_time  
    else:
        return bank_name, False, 'NO AUD data found'
    
    
def icbc():
    











driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(urls['abc'])
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

# 查找所有表格
tables = soup.find_all('table')
print(len(tables))



# # 获取第三个表格
third_table = tables[1]
#print(third_table)
# # 获取表格中的所有行
rows = third_table.find_all('tr')


# 查找澳元 (AUD) 的行
aud_row = None
for row in rows:
    cells = row.find_all('td')
    if cells and "澳大利亚元(AUD)" in cells[0].get_text():
        aud_row = row
        break

# 获取澳元的现汇卖出价
aud_exchange_rate = None
if aud_row:
    cells = aud_row.find_all('td')
    aud_exchange_rate = cells[3].get_text().strip() if len(cells) > 3 else "未找到现汇卖出价"

last_time = datetime.now()

if aud_exchange_rate and last_time:
    print("中国农业银行")
    print(f"澳元现汇卖出价: {aud_exchange_rate}")
    print(f"{last_time}")
else:
    print("Failed to find the Australian Dollar row or the expected data.")

driver.quit()


#boc
#success

# 获取中国银行汇率页面内容


#bocom
# -*- coding: utf-8 -*-
# @Time    : 2024/8/13 16:09
# @Author  : Nuaris





driver.get(urls['bocom'])
time.sleep(5)
content = driver.page_source


if content:
    soup = BeautifulSoup(content, 'html.parser')


 



third_table = soup.find('table')

rows = third_table.find_all('tr')


# 查找澳元 (AUD) 的行
aud_row = None
for row in rows:
    cells = row.find_all('td')
    if cells and "澳大利亚元(AUD/CNY)" in cells[0].get_text():
        aud_row = row


#print(aud_row)
cells = aud_row.find_all('td')

data = [cell.get_text(strip=True) for cell in cells]

aud_exchange_rate = data[3]
last_time = datetime.now()

if aud_exchange_rate and last_time:
    print("中国交通银行")
    print(f"澳元现汇卖出价: {aud_exchange_rate}")
    print(f"{last_time}")
else:
    print("Failed to find the Australian Dollar row or the expected data.")

driver.quit()


#ccb
# -*- coding: utf-8 -*-
# @Time    : 2024/8/13 16:09
# @Author  : Nuaris
# @File    : icbc_test
# @Software: Vscode
# @Description: 中国工商银行外汇牌价爬取
# debuging: 1. 无法获取到数据，原因是网页加载速度过慢，导致数据未加载完成，解决方法：增加等待时间
# status: updating



driver.get(urls['ccb'])
#WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//div[@class='cell' and text()='澳大利亚元(AUD)']")))
content = driver.page_source


if content:
    soup = BeautifulSoup(content, 'html.parser')

 
# 查找所有表格
if soup:
    lists = soup.find_all('ul')


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

#hsbc
#success


# 使用 WebDriver Manager 自动管理 ChromeDriver


driver.get(urls['hsbc'])
time.sleep(5)

content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

# 查找所有表格
tables = soup.find_all('table')


# 获取第三个表格
third_table = tables[2]

# 获取表格中的所有行
rows = third_table.find_all('tr')

# 查找最后更新时间
last_time_tag = None
for row in rows:
    last_time_tag = row.find('td', class_='ForTime01')
    if last_time_tag:
        break

last_time = last_time_tag.get_text().strip() if last_time_tag else "未找到最后更新时间"

# 查找澳元 (AUD) 的行
aud_row = None
for row in rows:
    cells = row.find_all('td')
    if cells and "澳元 (AUD)" in cells[0].get_text():
        aud_row = row
        break

# 获取澳元的现汇卖出价
aud_exchange_rate = None
if aud_row:
    cells = aud_row.find_all('td')
    aud_exchange_rate = cells[2].get_text().strip() if len(cells) > 3 else "未找到现汇卖出价"

if aud_exchange_rate and last_time:
    print("汇丰银行")
    print(f"澳元现汇卖出价: {aud_exchange_rate}")
    print(f"{last_time}")
else:
    print("Failed to find the Australian Dollar row or the expected data.")

driver.quit()

#icbc
# -*- coding: utf-8 -*-
# @Time    : 2024/8/13 16:09
# @Author  : Nuaris
# @File    : icbc_test
# @Software: Vscode
# @Description: 中国工商银行外汇牌价爬取
# debuging: 1. 无法获取到数据，原因是网页加载速度过慢，导致数据未加载完成，解决方法：增加等待时间
# status: updating



driver.get(urls['icbc'])
WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//div[@class='cell' and text()='澳大利亚元(AUD)']")))
content = driver.page_source

#print(content)
if content:
    soup = BeautifulSoup(content, 'html.parser')
#print(soup)

 

if soup:
    tables = soup.find_all('table')
else:
    print("fail to load contents")
    exit()



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

aud_exchange_rate = data[3]
last_time = data[5]

if aud_exchange_rate and last_time:
    print("中国工商银行")
    print(f"澳元现汇卖出价: {aud_exchange_rate}")
    print(f"{last_time}")
else:
    print("Failed to find the Australian Dollar row or the expected data.")

driver.quit()
