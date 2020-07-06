from selenium import webdriver
from selenium import common
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

"""
https://m.facebook.com/groups/skincarebyalana/ unaccessible
https://m.facebook.com/groups/607073569665649/ unaccessible
https://m.facebook.com/groups/1698970133500106/ accessible
https://m.facebook.com/groups/188297935057501/ unaccessible
https://m.facebook.com/groups/skincarebyalana/ unaccessible
"""

url = "https://m.facebook.com/groups/1698970133500106/"
driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.get(url)

# elems = driver.find_elements_by_class_name("story_body_container")
elems = driver.find_elements_by_xpath("//*[@class='_5rgt' or @class='_5nk5']")
for elem in elems:
    print(elem.text)
