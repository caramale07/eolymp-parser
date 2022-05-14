import requests
from bs4 import BeautifulSoup
import config
import openpyxl

URL = f"{config.url}login-check"
HEADERS = {"Content-type":"application/x-www-form-URLencoded"}
DATA = f"_username={config.username}&_password={config.password}"


table_data=[]

with requests.session() as s:
    s.post(URL, data=DATA, headers=HEADERS)
    page = s.get("https://www.eolymp.com/en/contests/25812/leaderboard", data=DATA,headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    table=soup.find_all('table')[0]
    
    thead = table.find('thead')
    head_row = thead.find_all('th')
    thead_data=[]
    for cell in head_row:
        thead_data.append(cell.text)
    
    tbody = table.find('tbody')
    body_rows = tbody.find_all('tr')
    tbody_data=[]
    for row in body_rows:
        row_data=[]
        for cell in row:
            row_data.append(cell.text)
        tbody_data.append(row_data)
    

table_data.append(thead_data)
for row in tbody_data:
    table_data.append(row)

"""  WRITING THE DATA TO THE .XLSX FILE  """

wb = openpyxl.Workbook()
    
sheet = wb.active 

for row in table_data:
    sheet.append(tuple(row))


wb.save('data.xlsx')
