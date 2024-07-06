import sqlite3
import pandas as pd


"""
sqlite3 를 통해 sql 쿼리를 수행하여 조회한 내용을 반환하는 함수
"""
def execute_sql(sql_text) -> list[any]:
    with sqlite3.connect('World_Economies.db') as conn:
        cur = conn.cursor()
        cur.execute(sql_text)
        rows = cur.fetchall()
        return rows


"""
국가,대륙 정보를 가지고 있는 region.txt 파일을 얼어
국가,대륙 정보를 가지고 있는 테이블 CONTINENT를 생성하는 함수
"""    
def create_nation_conti_table() -> None:
    txt_file = './region.txt'
    nation_conti_list = []
    with open(txt_file, mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # 줄 바꿈 문자 제거
            if line:
                nation, continent = line.split(',')
                nation_conti_list.append((nation, continent))
    
    with sqlite3.connect('World_Economies.db') as conn:
        cur = conn.cursor()
        cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS CONTINENT (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nation TEXT UNIQUE,
                continent TEXT
                )
                '''
        )
        
        for item in nation_conti_list:
            try:
                cur.execute(
                    '''
                    INSERT INTO CONTINENT (nation, continent) VALUES (?, ?)
                    ''',
                    (item[0], item[1])
                )
            except sqlite3.IntegrityError as e:
                print(e)
                break
            
        cur.execute(
                """
                CREATE TABLE IF NOT EXISTS NATION_CONTI  (
                nation TEXT PRIMARY KEY,
                gdp INTEGER,
                continent TEXT
                );
                """
        )