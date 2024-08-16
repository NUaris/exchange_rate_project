#success
import requests
from bs4 import BeautifulSoup



# 获取中国银行汇率页面内容
url = 'https://www.boc.cn/sourcedb/whpj/'
response = requests.get(url)
response.encoding = 'utf-8'  # 设置正确的编码

# 检查请求是否成功
if response.status_code != 200:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    exit()

# 解析页面内容
soup = BeautifulSoup(response.text, 'html.parser')

# 查找所有表格
tables = soup.find_all('table')

# 确认是否找到至少两个表格
if len(tables) < 2:
    print("Failed to find the second table.")
    exit()

# 获取第二个表格
second_table = tables[1]

# 查看找到的表格
#print(second_table)

rows = second_table.find_all('tr')

# 初始化变量以保存结果
third_value = None
last_time = None

# 查找澳大利亚元的汇率行
for row in rows:
    cells = row.find_all('td')
    if cells and cells[0].get_text().strip() == "澳大利亚元":
        # 打印找到的行以进行调试
        #print(row)
        third_value = cells[3].get_text().strip()  # 第三个数据
        last_time = cells[-2].get_text().strip()   # 倒数第二个数据
        break

if third_value and last_time:
    print("中国银行")
    print("汇率:", third_value)
    print("更新时间:", last_time)
else:
    print("Failed to find the Australian Dollar row or the expected data.")

def start():
    # 获取中国银行汇率页面内容
    url = 'https://www.boc.cn/sourcedb/whpj/'
    response = requests.get(url)
    response.encoding = 'utf-8'  # 设置正确的编码

    # 检查请求是否成功
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        exit()

    # 解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有表格
    tables = soup.find_all('table')

    # 确认是否找到至少两个表格
    if len(tables) < 2:
        print("Failed to find the second table.")
        exit()

    # 获取第二个表格
    second_table = tables[1]

    # 查看找到的表格
    #print(second_table)

    rows = second_table.find_all('tr')

    # 初始化变量以保存结果
    third_value = None
    last_time = None

    # 查找澳大利亚元的汇率行
    for row in rows:
        cells = row.find_all('td')
        if cells and cells[0].get_text().strip() == "澳大利亚元":
            # 打印找到的行以进行调试
            #print(row)
            third_value = cells[3].get_text().strip()  # 第三个数据
            last_time = cells[-2].get_text().strip()   # 倒数第二个数据
            break

    if third_value and last_time:
        print("中国银行")
        print("汇率:", third_value)
        print("更新时间:", last_time)
    else:
        print("Failed to find the Australian Dollar row or the expected data.")
