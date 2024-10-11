
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml
import csv
import time
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()

driver.get("https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1&orderBy=relevance/")

driver = webdriver.Chrome(executable_path='path_to_chromedriver')



# to close ok butten

shadow_host =webdriver(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#usercentrics-root")))

#acces the shadow
shadow_root= driver.execute_script('return argument[0].shadowRoot',shadow_host)

acccept_button= WebDriverWait(driver, 10).until(
     lambda d: shadow_root.find_element(By.CSS_SELECTOR, "button¨[data-testid='us-accept-all-button']")
)
acccept_button.click()

WebDriverWait(driver,10).until(EC.staleness_of(acccept_button))

search_button=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,'searchboxsubmintbutton')))
search_button.click()

time.sleep(1)


# Function to scrape a single property

def scrape_property(property_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    response = requests.get(property_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract data for the various fields
    property_data = {}
    
    try:
        property_data['Property ID'] = soup.find('div', {'class': 'classified__header--immoweb-code'}).text.strip()
    except AttributeError:
        property_data['Property ID'] = None
    
    try:
        property_data['Locality name'] = soup.find('span', {'span': 'aria-hidden="true"'}).text.strip()
    except AttributeError:
        property_data['Locality name'] = None
    
    try:
        property_data['Postal code'] = soup.find('span', {'class': 'classified__information'}).text.strip()
    except AttributeError:
        property_data['Postal code'] = None

    try:
        property_data['Price'] = soup.find('p', {'class': 'class":"classified__price'}).text.strip().replace("€", "").replace(",", "")
    except AttributeError:
        property_data['Price'] = None

    # Add other fields similarly...
    
    return property_data

# Test the function with a single property URL



property_url = "https://www.immoweb.be/en/"
property_info = scrape_property(property_url)
print(property_info)

# create cvs file

header =["Property ID","Locality name","Postal code","Price"]
house_list=[["Property ID",""],["Locality name",""],["Postal code",""],["Price", ""]]

with open("property_list.csv", "w") as myfile:
              wr=csv.writer(myfile)
              wr.writerow(header)
              wr.writerows(house_list)