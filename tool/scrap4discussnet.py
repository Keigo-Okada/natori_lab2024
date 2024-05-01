##coding == "utf-8"
#this code for discuss net

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

driver = webdriver.Chrome()
url = 'https://ssp.kaigiroku.net/tenant/kurashiki/MinuteSchedule.html?tenant_id=456&council_id=213&power_user=false&is_search=false&view_years=2011'
driver.get(url)
time.sleep(2)
links = driver.find_elements(By.CLASS_NAME, 'link-minute-view')
for i in range(0, len(links)):
    title = links[i].text
    match = re.search(r'(\d{2})月(\d{2})日', title)
    if match:
        month = match.group(1)
        day = match.group(2)
        formatted_date = f"{month}月{day}日"
        numbers = re.findall(r'\d+', formatted_date)
        title = ''.join(numbers)
        file_name = f"{title}.txt"
        time.sleep(1)

    links[i].click()
    time.sleep(6)
    driver.find_element(By.ID, "tab-minute-plain").click()
    elements = driver.find_elements(By.CLASS_NAME, 'info-txt')
    texts = []  
    time.sleep(1.5)
    for element in elements:
        texts.append(element.text) 
        text = '\n'.join(texts)

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write('\n'.join(texts))  

    driver.back()
    time.sleep(2)
else:
    print('終了しました。')
driver.quit()
