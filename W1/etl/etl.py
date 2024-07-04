import requests
from bs4 import BeautifulSoup
import pandas as pd
# import datetime as logger


"""
위키에서 국가별 GDP를 스크롤하여 리스트로 반환하는 함수
[[국가, GDP], [국가, GDP], ...] 형태
첫번째 행은 [모든 국가, GDP 총합]
"""
def scroll_wiki() -> list:
    # 데이터 저장을 위한 리스트 초기화
    table_data = [] 
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    response = requests.get(url)
    
    # 요청이 성공했는지 확인
    if response.status_code == 200:
        
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all('table')
        tbody = table[2].find('tbody')
        rows = tbody.find_all('tr')
    
        # 각 행의 데이터를 리스트 형태로 추출
        for row in rows:
            cells = row.find_all('td')[:2]
            if not cells:
                continue
            cell_values = [cell.get_text(strip=True) for cell in cells]
            if cell_values[1] == '\u2014':
                cell_values[1] = '-1'
            table_data.append(cell_values)
            
    # 요청 실패시 메시지 출력
    else:
        print("Failed to retrieve the web page")
    
    return table_data

"""
list 자료를 입력받아 json 파일로 내보내는 함수
"""
def list_to_json(_list) -> None:
    df = pd.DataFrame(_list)
    json_data = df.to_json(orient='records')
    
    with open('nation_gdp.json', 'w') as f:
        f.write(json_data)
    

def open_json() -> pd.DataFrame:
    json_path = './nation_gdp.json'
    df = pd.read_json(json_path)
    
    return df

def analyze(df):
    filtered_df = df[df[1].str.len()>=5][[0,1]]
    filtered_df = filtered_df[1:]
    filtered_df.rename(columns={0: 'Nation', 1: 'GDP'}, inplace=True)
    print(filtered_df)
    print(filtered_df.columns)
    # for i in filtered_list:
    #     print(i)
##

    
##
## wiki -- scraping --> jason
##
gdp_list = scroll_wiki()
list_to_json(gdp_list)

##
## json -- open, dataframe -> print
##
nation_gdp_df = open_json()
analyze(nation_gdp_df)