import time
import json
import random

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


DRIVER_PATH = "/Users/straw/Stuff/chromedriver"
URL = "http://127.0.0.1:5500/build_db/programmable_search_engine.html"
INP_FILE = 'words.txt'
OUT_FILE = 'words_image_url.txt'

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get(URL)
search_bar = driver.find_element(By.ID,'gsc-i-id1')

with open(INP_FILE, 'r') as inp:
    with open(OUT_FILE, 'a') as out:
        lines = inp.readlines()
        current_line = 7896
        last_line = len(lines)

        for i in range(current_line, last_line):
            result = {
                'word': lines[i].strip(),
                'inclusion_img_url': None
            }
            
            search_bar.clear()
            search_bar.send_keys(result['word'])
            search_bar.send_keys(Keys.ENTER)
            time.sleep(random.random() + 5)

            try:
                img = WebDriverWait(driver, timeout=3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'img.gs-image-scalable'))
                )
                img = driver.find_elements(By.CSS_SELECTOR, 'img.gs-image-scalable')[1]
                result['inclusion_img_url'] = img.get_attribute('src')
            except:
                pass
            out.write(f'{json.dumps(result)}\n')
    
# only close the tab
# driver.close()

# quit virtual browser
# driver.quit()