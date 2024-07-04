import requests
from bs4 import BeautifulSoup


##
## wiki -- scraping --> jason
##

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
response = requests.get(url)

# 요청이 성공했는지 확인
if response.status_code == 200:
    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table')
    tbody = table[2].find('tbody')
    rows = tbody.find_all('tr')
    
    # 데이터 저장을 위한 리스트 초기화
    table_data = [] 
    # 각 행의 데이터를 리스트 형태로 추출
    for row in rows:
        cells = row.find_all('td')[:2]
        # cells[0]
        # cells[1]
        # cells[2]
        cell_values = [cell.get_text(strip=True) for cell in cells]
        table_data.append(cell_values)
    for i in table_data:
        print(i)
    
    # 테이블의 모든 행(tr) 추출
    # rows = table.find_all('tr')
    # for row in rows:
    #     # 각 행의 모든 셀(td 또는 th) 추출
    #     cells = row.find_all(['td', 'th'])
    #     cell_values = [cell.get_text(strip=True) for cell in cells]
    #     print(cell_values)    
else:
    print("Failed to retrieve the web page")
    



##
## json -- open, dataframe -> print
##