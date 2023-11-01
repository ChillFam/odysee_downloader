from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
import time
import re

URL = "https://odysee.com"
downloadDirectory = ""
authToken = ""

# Create a headless Chrome instance
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", downloadDirectory)
driver = webdriver.Firefox(options=options)
w = WebDriverWait(driver, 20)

# Connect to odysee.com with user provided cookies
fileLinkList = []

driver.get(URL)
authCookie = {"name": "auth_token", "value": authToken, "domain": ".odysee.com", "path": "/"}
driver.add_cookie(authCookie)
driver.get(f"{URL}/$/following/manage")
time.sleep(5)
driver.refresh()

while True:
    channelLink = input("Enter odysee channel URL: ")
    print(f"\nNavigating to {channelLink}\n")
    driver.get(channelLink)
    fileLinkSelector = "icon.icon--Downloadable"
    w.until(ExpectedConditions.presence_of_element_located((By.CLASS_NAME, fileLinkSelector)))
    fileLinks = driver.find_elements(By.CLASS_NAME, fileLinkSelector)

    for fileLink in fileLinks:
        tempFileLink = fileLink.find_element(By.XPATH, "./../../../..")
        tempFileLink = tempFileLink.get_attribute("href")
        fileLinkList.append(tempFileLink)
       
    print(f"\nGot list of files for channel {channelLink}:\n {fileLinkList}\n")
    
    for fileLink in fileLinkList:
        driver.get(fileLink)
        downloadSelector = "button.button--primary"
        w.until(ExpectedConditions.presence_of_element_located((By.CLASS_NAME, downloadSelector)))
        downloadButton = driver.find_element(By.CLASS_NAME, downloadSelector).click()
        print(f"Downloading file {fileLink}")
        time.sleep(3)

    fileLinkList.clear()

    print("\nDownloads Complete")
