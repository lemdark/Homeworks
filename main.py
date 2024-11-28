from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json

def parse():
  driver = webdriver.Chrome()
  max_page = 2

  wait = WebDriverWait(driver, 10)

  result = []

  for page in range(1, max_page):
    driver.get(f'https://jobs.marksandspencer.com/job-search?page={page}&radius=')
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'border-1')))

    jobs = driver.find_elements(By.CLASS_NAME, 'border-1')
    for job in jobs:
        try:
            title_element = job.find_element(By.CLASS_NAME, 'text-2xl.bold.mb-16')
            url_element = job.find_element(By.CLASS_NAME, 'c-btn--primary')

            title = title_element.text.strip()
            url = url_element.get_attribute('href')
            result.append({
                'url': url,
                'title': title
            })
        except Exception as e:
            print(f"Error processing job: {e}")

    driver.quit()

    with open('result.json', 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    parse()
    print("Parsing completed. Results saved to result.json.")

