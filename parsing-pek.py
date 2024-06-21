from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import time
import csv 
import random

with open('/Users/svetlanaponamarenko/df_adress_pek.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = {}
    for row in reader:
      for key, value in row.items():
        if key in data:
          data[key].append(value)
        else:
          data[key] = [value]

def parsing_rewiews(dict_of_adress):
    list_links_of_rewiews = []
    list_links_error = []
    counter = 0
    for key, value in dict_of_adress.items():
        for el in value:
            if counter % 3 == 1:
                text = f'яндекс карты отзывы {key} {el}'
            elif counter % 3 == 3:
                text = f'яндекс карты {key} отзывы {el}'
            else:
                text = f'яндек карты {key} {el} отзывы'
               
            links_of_rewiews = {}
            links_error = {}
            counter += 1
            if counter % 4 == 0:
                time.sleep(random.uniform(70, 85))

            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
          
            chrome_option = Options()
            chrome_option.add_argument(f'{user_agent=}')
          
            driver = webdriver.Chrome(options=chrome_option)
            driver.get("https://www.rambler.ru")
            time.sleep(random.uniform(4, 9))
            search_box = driver.find_element(By.XPATH, "//input[@class='rc__QUSht rc__yjE3E']")
            time.sleep(random.uniform(1, 2))
            search_box.send_keys(text)
            time.sleep(random.uniform(2, 3))
            search_box.submit()
            time.sleep(11)
            print(counter, el)
            elements = driver.find_elements(By.XPATH, "//*[@id='client']/div/div/div[1]/div/section/article[1]/h2/a")
            for element in elements:
                link = element.get_attribute('href')
                if 'yandex.ru/maps' in link:
                    print(link)
                    if link[-2:-1].isdigit():
                        link = f'{link}reviews/'
                        links_of_rewiews['link'] = link
                        list_links_of_rewiews.append(links_of_rewiews)
                    else:
                        links_of_rewiews['link'] = link
                        list_links_of_rewiews.append(links_of_rewiews)
                else:
                    links_error['link'] = el
                    list_links_error.append(links_error)

            driver.quit()
            time.sleep(random.uniform(25, 40))
    return list_links_of_rewiews, list_links_error

list_links_of_rewiews, list_links_error = parsing_rewiews(data)

try:
  with open('pek_links_reviews.csv', 'r') as file:
    reader = csv.reader(file)
    existing_header = 1
except FileNotFoundError:
   existing_header = None

if existing_header is not None:
  with open('pek_links_reviews.csv', 'a', encoding='UTF-8', newline='') as f:
    csv_write = csv.DictWriter(f, fieldnames=['link'], delimiter=',')
    csv_write.writerows(list_links_of_rewiews)   
else:
   with open('pek_links_reviews.csv', 'w', encoding='UTF-8', newline='') as f:
    csv_write = csv.DictWriter(f, fieldnames=['link'], delimiter=',')
    csv_write.writeheader()
    csv_write.writerows(list_links_of_rewiews)  

try:
  with open('pek_links_error.csv', 'r') as file:
    reader = csv.reader(file)
    if reader:
      existing_header = 1
except FileNotFoundError:
   existing_header = None

if existing_header is not None:
  with open('pek_links_error.csv', 'a', encoding='UTF-8', newline='') as f:
    csv_write = csv.DictWriter(f, fieldnames=['link'], delimiter=',')
    csv_write.writerows(list_links_error)   
else:
   with open('pek_links_error.csv', 'w', encoding='UTF-8', newline='') as f:
    csv_write = csv.DictWriter(f, fieldnames=['link'], delimiter=',')
    csv_write.writeheader()
    csv_write.writerows(list_links_error)  

