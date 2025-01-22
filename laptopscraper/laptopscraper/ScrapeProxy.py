# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 01:00:10 2023

@author: Vu Lam Anh
"""

import requests
from bs4 import BeautifulSoup

# website to get free proxies
url = 'https://free-proxy-list.net/' 
 
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
#parser = fromstring(response.text)
# using a set to avoid duplicate IP entries.
proxies = set()

table = soup.find('table', class_ = "table table-striped table-bordered")
tbody = table.find('tbody')
trs = tbody.find_all('tr')
count = 0
for tr in trs:
    tds = tr.find_all('td')
    ip = tds[0].text
    port = tds[1].text
    proxies.add(ip+":"+port)
    


with open('ProxyList.txt', 'w') as f:
   f.write('\n'.join(proxies))
    