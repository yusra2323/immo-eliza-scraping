from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

driver.get("https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1&orderBy=relevance/")

driver = webdriver.Firefox(executable_path='path_to_chromedriver')


elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source




options = Options()
options.add_experimental_option("detach",True)

driver =webdriver.Chrome(Service=Service(ChromeDriverManager().install()),options=Options)


cookie_button = driver.find_element(By.XPATH, "//button[@data-testid='GDPR-accept']")
cookie_button.click()

driver.close()









