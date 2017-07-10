from selenium import webdriver
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from bs4 import BeautifulSoup
import re
import getpass


"""
Created by by James Gan: github.com/jamesylgan
Edited from cipavlou's linkedin-viewer-bot: https://github.com/cipavlou/linkedin-viewer-bot
"""

email = input("Enter your account email: ")
password = getpass.getpass("Enter your account password: ")
no_of_profiles = int(input("Enter how many LinkedIn profiles you wish to view? "))
keyword = input("Enter your search term: ")

def scraper():
    # Scrape page
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    page_urls = []
    for url in soup.find_all('a'):
        page_urls.append(str(url.get('href')))
    return page_urls
# Read from page.txt file to determine what pages already viewed
with open("page.txt", "r") as text_file:
    i = int(text_file.read())

page_max = round(no_of_profiles/10) + i

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

# Navigate to LinkedIn login page and log in
driver.get('https://linkedin.com/uas/login')
emailElement = driver.find_element_by_id('session_key-login')
emailElement.send_keys(email)
passElement = driver.find_element_by_id('session_password-login')
passElement.send_keys(password)
passElement.submit()
time.sleep(5)

# Look through profiles
profile_urls_storage = []
while i <= page_max:
    search_page_url = "https://www.linkedin.com/search/results/people/?keywords=" + keyword + "&origin=SUGGESTION&page=" + str(i) + "&title=" + keyword
    driver.get(search_page_url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i += 1
    time.sleep(5)
    urls_on_search_page = scraper()
    for url in urls_on_search_page:
        if ("/in/" in url):
            if url not in profile_urls_storage:
                profile_urls_storage.append(url)

    print("Got a page!")
    print(str(len(profile_urls_storage)) + " users to visit!")

num_profiles_visited = 0
for url in profile_urls_storage:
    driver.get("https://www.linkedin.com" + url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    num_profiles_visited += 1

print("Visited", num_profiles_visited, "profiles")
driver.quit()

# Write to page.txt file to keep track of how many pages viewed
with open("page.txt", "w") as text_file:
    text_file.write(str(i))