# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 16:47:51 2023

@author: USER
"""

import cx_Oracle as cx
import pandas as pd
# id, pw 보안을 위해 별도로 저장해둔 파일에서 가져옴
client_df = pd.read_csv('C:/Users/USER/Documents/client_secret.csv')
client_id = client_df['client_id'][1]
client_secret = client_df['client_secret'][1]
# oracle 설치 후 만들어둔 계정 사용
conn = cx.connect(client_id, client_secret, "127.0.01:1521/XE")

cur = conn.cursor()
# 기본으로 제공중인 employees table에 대해서 확인
cur.execute("select * from employees") #sql 쿼리 작성

for c in cur:
	print(c)
    
cur.close()
conn.close()

# remark : df = pd.read_sql 구문으로 불러옴
df = pd.read_sql("select * from employees where salary > 15000", con = conn)
