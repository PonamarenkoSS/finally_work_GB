from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import time
import csv 
import random
from selenium.webdriver.common.action_chains import ActionChains

with open('pek_links_reviews.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = {}
    for row in reader:
      for key, value in row.items():
        if key in data:
          data[key].append(value)
        else:
          data[key] = [value]

def pars(data, name):
    list_reviews = []
    for link in data['link']:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        chrome_option = Options()
        chrome_option.add_argument(f'{user_agent=}')
        
        driver = webdriver.Chrome(options=chrome_option)
        driver.get(link)

        time.sleep(random.uniform(17, 19))

        count_reviews = int(driver.find_elements(By.XPATH, "//div[@class='tabs-select-view__counter']")[-1].text)
        if count_reviews < 50:
           time.sleep(random.uniform(3, 5))
        elif count_reviews < 150:
            scrollable_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[7]/div/div[2]/div/div[1]/div[2]/div/div[3]/div[6]/div")    
            actions = ActionChains(driver)
            actions.move_to_element(scrollable_element).perform()
            time.sleep(random.uniform(15, 20))
        else:
           scrollable_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[7]/div/div[2]/div/div[1]/div[2]/div/div[3]/div[6]/div")    
           actions = ActionChains(driver)
           actions.move_to_element(scrollable_element).perform()
           time.sleep(random.uniform(80, 90))

        reviews = driver.find_elements(By.XPATH, "//span[@class='business-review-view__body-text']")
        for r in reviews:
            d = {}
            d['company'] = name
            d['review'] = r.text
            list_reviews.append(d)

        driver.quit()
        time.sleep(random.uniform(3, 5))

    return list_reviews

list_reviews = pars(data, 'ПЭК')

try:
  with open('reviews_sbor.csv', 'r') as file:
    reader = csv.reader(file)
    existing_header = 1
except FileNotFoundError:
   existing_header = None

if existing_header is not None:
  with open('reviews_sbor.csv', 'a', encoding='UTF-8', newline='') as f:
    csv_write = csv.DictWriter(f, fieldnames=['company', 'review'], delimiter=',')
    csv_write.writerows(list_reviews)   
else:
   with open('reviews_sbor.csv', 'w', encoding='UTF-8', newline='') as f:
    csv_write = csv.DictWriter(f, fieldnames=['company', 'review'], delimiter=',')
    csv_write.writeheader()
    csv_write.writerows(list_reviews)  


