#success
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime

chrome_options = Options()
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

driver.get(urls['abc'])
content = driver.page_source

#print(content)

soup = BeautifulSoup(content, 'html.parser')

# 查找所有表格
tables = soup.find_all('table')
print(len(tables))

# # 确认是否找到至少三个表格
# # if len(tables) < 3:
# #     print("Failed to find the third table.")
# #     driver.quit()
# #     exit()

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
