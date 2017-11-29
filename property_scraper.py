import requests
from bs4 import BeautifulSoup


"""
Scrapes data from century21 website and returns pertinent information before
initializing a pandas dataframe and writing the information to a .csv file
"""

# TODO:
# create pandas dataframe
# write information to .csv file
# get script to properly crawl through all the results/pages
# OPTIONAL: loop through individual property links to scrape for more detail
# OPTIONAL: utilize selenium

url = "https://www.century21.com/real-estate/salt-lake-city-ut/LCUTSALTLAKECITY/?"

r = requests.get(url)
c = r.content
soup = BeautifulSoup(c, "html.parser")

allElem = soup.find_all("div", {"class": "property-card-primary-info"})

allElem[0].find("a", {"class": "listing-price"}).text.replace("\n", "").strip()

for item in allElem:
    try:
        print(item.find("a", {"class": "listing-price"}).text.replace("\n", "").strip())
    except:
        print(None)
    try:
        print(item.find("div", {"class": "property-address"}).text.strip())
    except:
        print(None)
    try:
        print(item.find("div", {"class": "property-city"}).text.strip())
    except:
        print(None)
    try:
        print(item.find("div", {"class": "property-sqft"}).find("strong").text)
    except:
        print(None)
    try:
        print(item.find("div", {"class": "property-beds"}).find("strong").text)
    except:
        print(None)
    try:
        print(item.find("div", {"class": "property-baths"}).find("strong").text)
    except:
        print(None)
    try:
        print(item.find("div", {"class": "property-half-baths"}).find("strong").text)
    except:
        print(None)
    try:
        link = item.find("a", {"class": "listing-price"}).get('href')
        print(url + 'pdp=' + link[-12:])
    except:
        print(None)
    print()
