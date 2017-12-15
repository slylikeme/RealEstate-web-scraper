import pandas
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


"""
Scrapes data from century21 website and returns pertinent information before
initializing a pandas dataframe and writing the information to a .csv file.
User can scrape any city by changing the two variables: url AND base_url.

!!! Make sure to append "?" to url and "?p=" to base_url. !!!
"""

# empty list for storing list of dictionaries to be written to pandas dataframe
dictList = []

# change these two URLs to whatever city you wish to examine
# url for building links to individual properties
url = "https://www.century21.com/real-estate/salt-lake-city-ut/LCUTSALTLAKECITY/?"

# url for looping through pages of results
base_url = "http://www.century21.com/real-estate/salt-lake-city-ut/LCUTSALTLAKECITY/?p="

# Start the WebDriver
wd = webdriver.Firefox()

try:
    for page in range(1, 21, 1):
        print(base_url + str(page))

        # load the page
        wd.get(base_url + str(page))

        # set page to grid view
        grid_select = wd.find_element_by_css_selector('.grid-background')
        grid_select.click()
        time.sleep(1.0)

        # Wait for the dynamically loaded elements to show up
        SCROLL_PAUSE_TIME = 1.5

        # Get scroll height
        last_height = wd.execute_script("return document.body.scrollHeight")

        # while loop that scrolls to bottom of page
        while True:
            # Scroll down to bottom
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = wd.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Grab the page HTML source
        html_page = wd.page_source

        # Now use html_page in bs4
        soup = BeautifulSoup(html_page, "html.parser")

        # scrape for property info and set to variable
        allElem = soup.find_all("div", {"class": "property-card-primary-info"})

        for item in allElem:
            d = {}
            try:
                d["Price"] = item.find("a", {"class": "listing-price"}).text.replace("\n", "").strip()
            except:
                d["Price"] = None
            try:
                d["Address"] = item.find("div", {"class": "property-address"}).text.strip()
            except:
                d["Address"] = None
            try:
                d["Locality"] = item.find("div", {"class": "property-city"}).text.strip()
            except:
                d["Locality"] = None
            try:
                d["Sq. Feet"] = item.find("div", {"class": "property-sqft"}).find("strong").text
            except:
                d["Sq. Feet"] = None
            try:
                d["Beds"] = item.find("div", {"class": "property-beds"}).find("strong").text
            except:
                d["Beds"] = None
            try:
                d["Full Baths"] = item.find("div", {"class": "property-baths"}).find("strong").text
            except:
                d["Full Baths"] = None
            try:
                d["Half Baths"] = item.find("div", {"class": "property-half-baths"}).find("strong").text
            except:
                d["Half Baths"] = None
            try:
                link = item.find("a", {"class": "listing-price"}).get('href')
                d["URL"] = url + 'pdp=' + link[-12:]
            except:
                d["URL"] = None
            dictList.append(d)

        # click to next page if available
        next_page = wd.find_element_by_css_selector('#pagination-next')
        next_page.click()
        time.sleep(1.0)

# end scraping when out of pages
except NoSuchElementException:
    print("No more pages!")
    pass

# write dictList to dataframe, then write dataframe to csv file in current directory
df = pandas.DataFrame(dictList)
df.to_csv("PropertyInfo.csv")

# close web driver
wd.quit()
