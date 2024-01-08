# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 14:21:39 2024

@author: USER
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import json
job_df = pd.DataFrame(columns = ['company_name', 'descriptions','date',
                                 'industry', 'category', 'title'])
cur_row = 0
i = 198001
while cur_row < 5000:
    i -= 1
    link = 'https://www.wanted.co.kr/wd/' + str(i)
    resp = requests.get(link)
    html = resp.text
    soup = bs(html, 'lxml')

    # title, position, main_tasks, requirements, sub_categories, company_name
    # script에 원하는 정보가 담겨있다.

    try:
        contents = soup.find('script',attrs={'type':'application/ld+json'}).text
        contents = json.loads(contents)
        company_name = contents['hiringOrganization']['name']
        descriptions = contents['hiringOrganization']['description']
        date = contents['datePosted']
        industry = contents['industry']
        category = contents['occupationalCategory']
        title = contents['title']
        cur_list = [company_name, descriptions, date,
                                 industry, category, title]
        job_df.loc[cur_row]=cur_list
        cur_row += 1
        #print('%s %s input' %(company_name, category))
    except:
        pass

job_df.to_csv('C:/Users/USER/Desktop/personal_project/wanted_crawling.csv',
              encoding = 'utf-8-sig', index = False)


