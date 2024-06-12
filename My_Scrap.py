from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import simplejson as json


def wait_element(browser, delay_seconds=1, by=By.CLASS_NAME, value=None):
    return WebDriverWait(browser, delay_seconds).until(
        expected_conditions.presence_of_element_located((by, value))
    )


chrome_path = ChromeDriverManager().install()
options = ChromeOptions()
options.add_argument("--headless")
browser_service = Service(executable_path=chrome_path)
browser = Chrome(service=browser_service, options=options)
browser.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2")

vakancy_list_tag = browser.find_element(By.ID, "a11y-main-content")
vakancy_tags = vakancy_list_tag.find_elements(By.TAG_NAME, 'h2')

links = []
for vakancy in vakancy_tags:
    links.append(wait_element(vakancy, by=By.TAG_NAME, value="a").get_attribute("href"))

data = []
for link in links:
    browser.get(link)

    # зп
    salary_tag = browser.find_element(by=By.CLASS_NAME, value="vacancy-title")
    taga = salary_tag.find_elements(By.TAG_NAME, 'div')
    salary_text = taga[1].text

    # company
    company_name = wait_element(browser, by=By.CLASS_NAME, value="vacancy-company-name").text

    # city
    city_name = browser.find_element(by=By.CLASS_NAME, value="vacancy-company-redesigned")
    city_tag = city_name.find_elements(by=By.TAG_NAME, value='div')
    city = city_tag[-1].text

    #text
    text_info = browser.find_element(by=By.CLASS_NAME, value="g-user-content")
    text = text_info.text
    if 'Django' in text or 'django' in text or 'Flask' in text or 'flask' in text:
        data.append({'link': link, 'salary': salary_text, 'company': company_name, 'city': city})

with open('new.json', 'w') as f:
    json.dump(data, f)


