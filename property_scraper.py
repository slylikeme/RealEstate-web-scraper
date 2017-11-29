import requests
import pandas
from bs4 import BeautifulSoup


"""
Scrapes data from century21 website and returns pertinent information before
initializing a pandas dataframe and writing the information to a .csv file
"""

# TODO:
# get script to properly crawl through all the results/pages
# OPTIONAL: loop through individual property links to scrape for more detail
# OPTIONAL: utilize selenium

url = "https://www.century21.com/real-estate/salt-lake-city-ut/LCUTSALTLAKECITY/?"

r = requests.get(url)
c = r.content
soup = BeautifulSoup(c, "html.parser")

allElem = soup.find_all("div", {"class": "property-card-primary-info"})

dictList = []
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

df = pandas.DataFrame(dictList)
df.to_csv("PropertyInfo.csv")
