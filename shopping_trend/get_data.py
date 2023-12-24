# data get
# 목표 : 네이버 api를 활용한 검색어 데이터 get 및 전처리
import requests
import json
import pandas as pd

client_df = pd.read_csv('C:/Users/USER/Documents/client_secret.csv')
client_id = client_df['client_id'][0]
client_secret = client_df['client_secret'][0]

def get_result(startDate, endDate, timeUnit, category, device, gender, ages):
    url = 'https://openapi.naver.com/v1/datalab/shopping/categories'

    header = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret,
        'Content-Type': 'application/json'
    }

    body_dict = {}
    body_dict['startDate'] = startDate
    body_dict['endDate'] = endDate
    body_dict['timeUnit'] = timeUnit
    body_dict['category'] = category
    body_dict['device'] = device
    body_dict['gender'] = gender
    body_dict['ages'] = ages

    response = requests.post(url, json=body_dict, headers = header)
    response_code = response.status_code
    print(response_code)
    return response

startDate='2023-06-01'
endDate='2023-09-30'
timeUnit='month'  #'date','week','month'
category=[
    {'name':'패션의류', 'param':['50000000']},
    # 세부 품목별 카테고리 가능, 다만 이것에 대해서 정확한 이름을 붙여야함
    # 직접 검색을 통해 확인해야 한다고 가이드에 적혀 있어 대상을 한정하여 검색 필요
    {'name': '식품', 'param':['50007077']}
]
device='pc'  #'pc','mo'
gender='m,f'   #'m','f'
ages=['20']  #10, 20, 30, 40, 50, 60(60은 60세 이상)

result = get_result(startDate,endDate,timeUnit,category,device,gender,ages)

# json을 dataframe 형태로 저장하여 바꾸기 -> json_normalize
