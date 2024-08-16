#success
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  # 无界面模式
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 使用 WebDriver Manager 自动管理 ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get('https://www.services.cn-banking.hsbc.com.cn/PublicContent/common/rate/zh/exchange-rates.html')
time.sleep(5)

content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

# 查找所有表格
tables = soup.find_all('table')

# 确认是否找到至少三个表格
# if len(tables) < 3:
#     print("Failed to find the third table.")
#     driver.quit()
#     exit()

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
