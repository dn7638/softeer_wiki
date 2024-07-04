from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime as logger


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
    df.rename(columns={0: 'Nation', 1: 'GDP'}, inplace=True)
    # GDP가 100 이상인 행들을 추출하여 출력
    filtered_df = df[df['GDP'].str.len()>=5][['Nation','GDP']]
    filtered_df = filtered_df[1:]
    print('[Nations with GDP exceeding 100B USD]')
    print(filtered_df)
    
    
    nation_continent_dict, continent_GDP_dict = trans_region_data()
    
    df_sorted = df.sort_values(by='GDP')
    for index, row in df_sorted.iterrows():
        nation, gdp = row['Nation'], row['GDP']
        if nation_continent_dict.get(nation):
            continent_GDP_dict[nation_continent_dict[nation]].append(gdp)
    
    print('Top 5 GDP averages in each region')
    for key, value in continent_GDP_dict.items():
        value_int = [int(num.replace(',','')) for num in value]
        avg = 0
        if len(value_int) > 4:
            avg = sum(value_int[0:5])//5
        else:
            avg = sum(value_int)//len(value_int)
        avg = format(avg, ",")
        print(f'{key:15} : {avg}')
        
        
def trans_region_data() -> tuple[dict, dict]:
    # 텍스트 파일 경로
    txt_file = 'region.txt'

    # 빈 dictionary 생성
    nation_continent_dict = dict()
    continent_set = set()

    # 텍스트 파일 읽기
    with open(txt_file, mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # 줄 바꿈 문자 제거
            if line:
                nation, continent = line.split(',')
                nation_continent_dict[nation] = continent
                continent_set.add(continent)
                
    continent_GDP_dict = {item : [] for item in continent_set}

    return nation_continent_dict, continent_GDP_dict
    
    
    
################################
## wiki -- scraping --> jason ##
################################

#E : start extract
gdp_list = scroll_wiki()
#E : end extract

#T : start transform (list -> json)
list_to_json(gdp_list)
#T : end transform (list -> json)

######################################
## json -- open, dataframe -> print ##
######################################

#L : start load
nation_gdp_df = open_json()
#L : end load

analyze(nation_gdp_df)