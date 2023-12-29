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

# 2023.01.01 ~ 2023.11.30 11개월간의 분석 진행

startDate='2023-01-01'
endDate='2023-11-30'
timeUnit='month'  #'date','week','month'
category=[
    # 세부 품목별 카테고리 가능, 다만 이것에 대해서 정확한 이름을 붙여야함
    # 직접 검색을 통해 확인해야 한다고 가이드에 적혀 있어 대상을 한정하여 검색 필요
    # 3개 이상의 분류 사용 금지 -> 여러개를 나눠서 저장하는 방식으로 코드 구성 필요
    # 효율적인 분석을 위한 가설 설정 필요
    {'name':'패션의류', 'param':['50000000']},
    {'name':'가전', 'param':['50000210']},
    {'name':'화장품/미용', 'param':['50000002']},   
]
device='pc'  #'pc','mo'
gender='m'   #'m','f'
ages=['20', '30']  #10, 20, 30, 40, 50, 60(60은 60세 이상)

result = get_result(startDate,endDate,timeUnit,category,device,gender,ages)

# json을 dataframe 형태로 저장하여 바꾸기 -> json_normalize

result_json = result.json()
# json normalize를 진행 -> result_data에 category별로 저장이 되는 구조
# normalize를 기반으로 
result_df = pd.json_normalize(data = result_json['results'],
                              record_path = 'data',
                              meta = ['title', 'category'])
# 문제 : 20대 남성과 20대 여성 등 집단별 절대적 클릭 숫자 비교 불가능
# 다른 형식의 가설이 필요하다.
result_df.to_csv('C:/Users/USER/Desktop/personal_project/shopping_trend/2030_trend_bigcat.csv')