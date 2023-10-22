from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
import time
import re

URL = "https://odysee.com"
authCookieValue = ""
downloadDirectory = r""

# Define a function that creates a headless Firefox instance and returns the driver object
def create_driver(download_directory):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", download_directory)
    driver = webdriver.Firefox(options=options)
    return driver

# Define a function that connects to odysee.com with user provided cookies and returns the driver object
def connect_to_odysee(driver, url, auth_cookie_value):
    # Connect to odysee.com with user provided cookies
    print(f"Navigating to {url}\n")
    driver.get(url)
    authCookie = {"name": "auth_token", "value": auth_cookie_value, "domain": ".odysee.com", "path": "/"}
    driver.add_cookie(authCookie)
    driver.get(f"{url}/$/following/manage")
    time.sleep(20)
    driver.refresh()
    return driver

# Define a function that prints the output of the selector by class name and returns a list of subscription links
def get_subscription_links(driver, selector):
    # Print the output of the selector by class name
    w = WebDriverWait(driver, 60)
    w.until(ExpectedConditions.presence_of_element_located((By.CLASS_NAME, selector)))
    subscriptions = driver.find_elements(By.CLASS_NAME, selector)

    # Filter the HTML for subscription links
    links = []

    for sub in subscriptions:
        link = sub.find_element(By.TAG_NAME, "a")
        link = link.get_attribute('href')
        links.append(f"{link}?view=content")

    print(f"Got list of channel subscriptions:\n {links}\n")
    return links

# Define a function that gets file links and downloads them for a given channel link
def download_files(driver, link):
    # Get file links and download them
    fileLinkSelector = "icon.icon--Downloadable"
    fileLinkList = []
    
    driver.get(link)
    time.sleep(3)
    
    fileLinks = driver.find_elements(By.CLASS_NAME, fileLinkSelector)
    
    for fileLink in fileLinks:
        tempFileLink = fileLink.find_element(By.XPATH, "./../../../..")
        tempFileLink = tempFileLink.get_attribute("href")
        fileLinkList.append(tempFileLink)
       
    print(f"\nGot list of files for channel {link}:\n {fileLinkList}\n")
    
    w = WebDriverWait(driver, 60)
    
    for fileLink in fileLinkList:
        try:
            driver.get(fileLink)
            downloadSelector = "button.button--primary"
            w.until(ExpectedConditions.presence_of_element_located((By.CLASS_NAME, downloadSelector)))
            downloadButton = driver.find_element(By.CLASS_NAME, downloadSelector).click()
            print(f"Downloading file {fileLink}")
            time.sleep(1)
        except Exception as e:
            print(f"An error occurred while downloading file {fileLink}: {e}")
            continue

# Define the main function that calls the other functions and executes the script
def main():
    
    # Create a headless Firefox instance
    try:
        driver = create_driver(downloadDirectory)
        print("Driver created successfully.")
    except Exception as e:
        print(f"An error occurred while creating driver: {e}")
        return
    
    # Connect to odysee.com with user provided cookies
    try:
        driver = connect_to_odysee(driver, URL, authCookieValue)
        print("Connected to odysee.com successfully.")
    except Exception as e:
        print(f"An error occurred while connecting to odysee.com: {e}")
        return
    
    # Get subscription links
    try:
        links = get_subscription_links(driver, "claim-preview.claim-preview--channel")
        print("Got subscription links successfully.")
    except Exception as e:
        print(f"An error occurred while getting subscription links: {e}")
        return
    
    # Download files for each channel link
    for link in links:
        download_files(driver, link)

    print("\nDownloads Complete")

# Call the main function
if __name__ == "__main__":
   main()