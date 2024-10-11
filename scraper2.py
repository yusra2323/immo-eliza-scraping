
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import lxml
import csv
import time
from bs4 import BeautifulSoup
import pandas as pd
import os
import pandas as pd


driver = webdriver.Firefox()



driver.get("https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1&orderBy=relevance/")

driver = webdriver.Chrome(executable_path='path_to_chromedriver')


elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()




options = Options()
options.add_experimental_option("detach",True)

driver =webdriver.Chrome(Service=Service(ChromeDriverManager().install()),options=Options)


cookie_button = driver.find_element(By.XPATH, "//button[@data-testid='GDPR-accept']")
cookie_button.click()




def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None

# Function to scrape property details from HTML
    


def scrape_property(html):
    
    soup = BeautifulSoup(html, 'html.parser')

    # Extract data for the various fields
    property_data = {}
    try:
        property_data['Property ID'] = soup.find('div', {'class': 'classified__header--immoweb-code'}).text.strip()
    except AttributeError:
        property_data['Property ID'] = None

    try:
         property_data['Locality name'] = soup.find('div', {'class': 'classified__information--address'}).text.strip()
    except AttributeError:
        property_data['Locality name'] = None

    try:
        property_data['Postal code'] = soup.find('span', {'class': 'classified__information--address-row'}).text.strip()
    except AttributeError:
        property_data['Postal code'] = None

    try:
        property_data['Price'] = soup.find('span', {'class': 'sr-only'}).text.strip().replace("€", "").replace(",", "")
    except AttributeError:
        property_data['Price'] = None

    try:
        property_data['Room no'] = soup.find('span', {'class': 'overview__text'}).text.strip()
    except AttributeError:
        property_data['Room no'] = None

    try:
        property_data['Living area'] = soup.find('div', {'class':'classified-table__data'}).text.strip()
    except AttributeError:
        property_data['Living area'] = None

    try:
        property_data['Equipped kitchen'] = soup.find('div', {'class': 'classified-table__data'}).text.strip()
    except AttributeError:
        property_data['Equipped kitchen'] = None
    try:
        property_data['Terrace'] = soup.find('div', {'class': 'classified-table__data'}).text.strip()
    except AttributeError:
        property_data['Terrace'] = None

    try:
        property_data['Garden'] = soup.find('div', {'class': 'classified-table__data'}).text.strip()
    except AttributeError:
        property_data['Garden'] = None
    try:
        property_data['Swimming pool'] = soup.find('div', {'class': 'classified-table__header'}).text.strip()
    except AttributeError:
        property_data['Swimming pool'] = None
    return property_data


# Test the function with a single property URL
url =" https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/oudenaarde/9700/20235435"
property_info = scrape_property(url)
print(property_info)


 # List of XML URLs to download
urls = [
    "https://assets.immoweb.be/sitemap/classifieds-000.xml",
    "https://assets.immoweb.be/sitemap/classifieds-001.xml",
    "https://assets.immoweb.be/sitemap/classifieds-002.xml",
    "https://assets.immoweb.be/sitemap/classifieds-003.xml",
    "https://assets.immoweb.be/sitemap/classifieds-004.xml",
    "https://assets.immoweb.be/sitemap/classifieds-005.xml",
    "https://assets.immoweb.be/sitemap/classifieds-006.xml",
    "https://assets.immoweb.be/sitemap/classifieds-007.xml",
    "https://assets.immoweb.be/sitemap/classifieds-008.xml",
    "https://assets.immoweb.be/sitemap/classifieds-009.xml",
    "https://assets.immoweb.be/sitemap/classifieds-010.xml",
    "https://assets.immoweb.be/sitemap/classifieds-011.xml",
    "https://assets.immoweb.be/sitemap/classifieds-012.xml",
    "https://assets.immoweb.be/sitemap/classifieds-013.xml",
    "https://assets.immoweb.be/sitemap/classifieds-014.xml",
    "https://assets.immoweb.be/sitemap/classifieds-015.xml",
    "https://assets.immoweb.be/sitemap/classifieds-016.xml",
    "https://assets.immoweb.be/sitemap/classifieds-017.xml",
    "https://assets.immoweb.be/sitemap/classifieds-018.xml",
    "https://assets.immoweb.be/sitemap/classifieds-019.xml",
    "https://assets.immoweb.be/sitemap/classifieds-020.xml",
    "https://assets.immoweb.be/sitemap/classifieds-021.xml",
    "https://assets.immoweb.be/sitemap/classifieds-022.xml",
    "https://assets.immoweb.be/sitemap/classifieds-023.xml",
    "https://assets.immoweb.be/sitemap/classifieds-024.xml",
    "https://assets.immoweb.be/sitemap/classifieds-025.xml",
    "https://assets.immoweb.be/sitemap/classifieds-026.xml",
    "https://assets.immoweb.be/sitemap/classifieds-027.xml",
    "https://assets.immoweb.be/sitemap/classifieds-028.xml",
    "https://assets.immoweb.be/sitemap/classifieds-029.xml",
    "https://assets.immoweb.be/sitemap/cms-000.xml",
    "https://assets.immoweb.be/sitemap/customers-000.xml",
    "https://assets.immoweb.be/sitemap/static-000.xml",
    "https://assets.immoweb.be/sitemap/static-001.xml",
    "https://assets.immoweb.be/sitemap/static-002.xml",
    "https://assets.immoweb.be/sitemap/static-003.xml",
    "https://assets.immoweb.be/sitemap/static-004.xml",
]
 
# Directory to save XML files
os.makedirs('xml_files', exist_ok=True)
 
all_urls = []
 
# Download and parse each XML file
for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        file_path = os.path.join('xml_files', url.split('/')[-1])
 
        # Save the XML file
        with open(file_path, 'wb') as file:
            file.write(response.content)
 
        # Parse the XML file
        soup = BeautifulSoup(response.content, 'xml')
 
        # Extract URLs (adjust the tag name based on the XML structure)
        loc_tags = soup.find_all('loc')
        for loc in loc_tags:
            all_urls.append(loc.text)
 
    except Exception as e:
        print(f"Error downloading or parsing {url}: {e}")
 
# Create a DataFrame and save to CSV
df = pd.DataFrame(all_urls, columns=['url'])
df.to_csv('xml_files/extracted_urls.csv', index=False)



# Load URLs from the CSV file
url_file_path = r"C:\Users\yusra\OneDrive\Documents\GitHub\immo-eliza-scraping\immoeliza\xml_files\extracted_urls.csv"

urls_df = pd.read_csv(url_file_path)

# Assume the URLs are in a column named 'url'
urls = urls_df['url'].head(10).tolist()  # Get only the first 10 URLs

# Initialize an empty list to store the results
results = []

# Loop through each URL and scrape the data
for url in urls:
    html = get_html(url)
    if html:
        property_data =  property(html)
        results.append(property_data)  # Append the details to the results list
    else:
        print(f"Failed to retrieve HTML for {url}")



# Convert to DataFrame and save to CSV
df = pd.DataFrame(property_info ,index=[0])
df.to_csv('real_estate_data.csv', index = False)