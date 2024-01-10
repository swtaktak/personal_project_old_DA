# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:55:52 2024

@author: USER
"""

import pandas as pd
import re

job_df = pd.read_csv('C:/Users/USER/Desktop/personal_project/wanted_JD_analysis/wanted_crawling.csv',
              encoding = 'utf-8-sig')
# 공고 재업로드 등으로 인해 완벽하게 같은 공고가 들어 왔을 수 있음
# 그러나 drop을 실시하면 안 되는 것이, 수요 재발생 등의 고려 필요
# job_df = job_df.drop_duplicates().reset_index(drop = True)
# 전처리 계획
# 1) date : 연-월만 있어도 분석에 충분
# 2) category : 대분류>중분류>... 방식, 전체적으로 중분류만 있어도 충분
# 3) descriptions : 주요 업무, 자격 요건, 우대 사항만 추출 방법...
# 방법 : 주요 업무 ~ 혜택 및 복지 전까지만 추출하면 됨
# 그 이후 구분 방법을 찾아 효율적 구분 필요

# 
job_df['dt_ym'] = job_df.date.apply(lambda x : x[0:7])
job_df['ct_brief'] = job_df.category.apply(lambda x : list(x.split(','))[0:2])
job_df['job_due'] = job_df.descriptions.apply(lambda x: x[x.find('주요업무')+5: 
                                                         x.find('자격요건')])
job_df['job_due'] = job_df.job_due.apply(lambda x : list(x.split('\n')))
job_df['job_req'] = job_df.descriptions.apply(lambda x: x[x.find('자격요건')+5: 
                                                         x.find('우대사항')])
job_df['job_req'] = job_df.job_req.apply(lambda x : list(x.split('\n')))
job_df['job_add'] = job_df.descriptions.apply(lambda x: x[x.find('우대사항')+5: 
                                                         x.find('혜택 및 복지')])
job_df['job_add'] = job_df.job_add.apply(lambda x : list(x.split('\n')))
# 대분류, 소분류를 미리 만들자.
job_df['ct_1st'] = job_df.ct_brief.apply(lambda x : x[0])
job_df['ct_2nd'] = job_df.ct_brief.apply(lambda x : x[1].strip())
# 마지막으로 필요없는 항목에 대한 제거 실시
job_df = job_df[['company_name','industry', 'dt_ym', 'ct_1st','ct_2nd', 
                      'job_req', 'job_add', 'job_due', 'title']]

def del_special_letter(s):
    # 한글, 숫자, 영어, 띄어쓰기만 살아남기고 모두 지워버리는 정규표현식
    new_str = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", s)
    return new_str

def handle_space(s_list):
    for i in range(len(s_list)):
        s_list[i] = s_list[i].strip()
    while '' in s_list:
        s_list.remove('')
    return s_list
            
        
job_df['job_due'] = job_df.job_due.apply(lambda x: [del_special_letter(s) for s in x])
job_df['job_due'] = job_df.job_due.apply(lambda x: handle_space(x))
job_df['job_req'] = job_df.job_req.apply(lambda x: [del_special_letter(s) for s in x])
job_df['job_req'] = job_df.job_req.apply(lambda x: handle_space(x))
job_df['job_add'] = job_df.job_add.apply(lambda x: [del_special_letter(s) for s in x])
job_df['job_add'] = job_df.job_add.apply(lambda x: handle_space(x))

# 특수문자와 다양한 것들에 대해 제외 처리 완료.
# Next step : 불용어 처리 및, 중복단어 제거로 핵심어만 추출
# TF-IDF 활용하여 할 수 있을까? / keywordrank 등의 사용도 고려

# step / 한국어 전처리 후, 명사 태깅 사용 -> 해당 명사로 빈도분석 실시
# 주요 어휘가 무엇인지 등등을 보는 것이므로, 명사만 가져와야 유의미함
# 같은 단어가 반복해서 나온다면 중요한 것이므로 굳이 중복이라고 지우지 말 것
# 불용어 사전을 정의해서 쓰자. 1글자만 하기에는 딥러닝 등의 변수가 있어 불가
# 추가로 각종 공고에서 반복적으로 쓰이나 큰 차별화 단어가 아닌 단어도 포함한다.

stop_words = ['및', '은', '는', '이', '가', '을', '를', '등', '로', '와','준',
              '과', '수', '각', '각각', '의', '더', '사람', '같', '아니', '분',
              '경험', '유관', '업무', '대한', '사', '근무', '우대', '필수', '그',
              '역량', '일', '저', '통한', '것', '사용', '이해', '보유', '이해도',
              '능력', '이상', '자격', '대해', '기간', '저희', '이번', '통해', '중', 
              '관련', '수행', '기반', '해', '요원', '필요', '위', '최소']
from konlpy.tag import Okt
okt = Okt()
def get_noun_list(s):
    noun_list = []
    for cur_s in s:
        cur_nouns = okt.nouns(cur_s)
        noun_list += cur_nouns
    return [n for n in noun_list if n not in stop_words]

job_df['job_due_noun'] = job_df.job_due.apply(lambda x : get_noun_list(x))
job_df['job_req_noun'] = job_df.job_req.apply(lambda x : get_noun_list(x))
job_df['job_add_noun'] = job_df.job_add.apply(lambda x : get_noun_list(x))

# 이제 남은 것으로 빈도 분석 등을 진행하고 언어 분석 등 다른 것을 진행할거라
# 전처리 대신 이제 실제 분석으로 진행한다.
job_df_final = job_df[['company_name','industry', 'dt_ym', 'ct_1st','ct_2nd', 
                      'job_req_noun', 'job_add_noun', 'job_due_noun', 'title']]
job_df_final.to_csv('C:/Users/USER/Desktop/personal_project/wanted_JD_analysis/wanted_data_prep.csv',
              encoding = 'utf-8-sig', index = False)
print('end of preprocessing')