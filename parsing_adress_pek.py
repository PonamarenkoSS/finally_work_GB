import pandas as pd
import requests
import urllib.parse
import pandas as pd
from lxml import html
import time
import random

url = 'https://pecom.ru/contacts/list-filials/'

response = requests.get(url, headers = \
    {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})

print(response.status_code)

def pars_address_pek(url):
    response = requests.get(url, headers = \
    {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        try:
            xpath = (".//*[@id='filial_cities']/a", ".//*[@id='filial_cities']/div/a") #два пути, т.к. для первых городов каждой буквы алфавита пути отличаются от пути по остальным городам
        except:
            print('Error')
        names = []
        links = []    
        for path in xpath:
            try:
                rows = tree.xpath(path)
            except:
                print('Error')
            for i in range(len(rows)):
                try:
                    names.append(rows[i].xpath(".//text()")[0])
                except:
                    print('Error')
                try:
                    links.append(rows[i].xpath(".//@href")[0])
                except:
                    print('Error')
        url_joined = []
        for link in links:
            url_joined.append(urllib.parse.urljoin('https://pecom.ru', link))
        return names, url_joined
    else:
        print(f'Error - {response.status_code}')


names_pek, url_joined_pek = pars_address_pek(url)

print(f'{len(url_joined_pek)=}, {len(url_joined_pek)=}')

def get_adress(name_of_company, url_of_cities):
    adress_of_company = {name_of_company : []}
    error = []
    min_wait_time = 3
    max_wait_time = 8
    count = 1
    for url in url_of_cities:
        response2 = requests.get(url, headers = \
    {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})
        if response2.status_code == 200:
            tree = html.fromstring(response.content)
            try:
                rows = tree.xpath(".//*[@id='page']/div[2]/div/div[2]/div[2]/div[1]/div/div")
                try: 
                    list_of_adress = rows[1].xpath(".//span/text()")
                except:
                    error.append(url)
                    time.sleep(random.uniform(min_wait_time, max_wait_time))   
                    
                for el in list_of_adress:
                    adress_of_company[name_of_company].append(el)
                time.sleep(random.uniform(min_wait_time, max_wait_time))

            except KeyError:
                error.append(url)
                time.sleep(random.uniform(min_wait_time, max_wait_time))
                continue
        else:
            error.append(url)
            time.sleep(random.uniform(min_wait_time, max_wait_time))
            continue
        print(f'done {count}')
        count+=1
    return adress_of_company, error

adress_of_company, error_lst = get_adress('ПЭК', url_joined_pek)

print(len(adress_of_company))

df_adress_pek = pd.DataFrame(adress_of_company)

print(df_adress_pek.head())

df_adress_pek.to_csv('df_adress_pek.csv', index=False)