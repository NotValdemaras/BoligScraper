from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import os
import uuid



#Setting uo location options
def scrape():

    #Setting up Selenium driver
    options = webdriver.ChromeOptions()
    options.binary_location = 'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'
    options.add_argument("--headless")
    chrome_driver_binary = 'D:\MyPrograms\Anaconda\envs\scraper\Lib\site-packages\chromedriver_binary\chromedriver.exe'
    driver = webdriver.Chrome(chrome_driver_binary, options=options)


    #Download HTML
    #myurl = 'https://www.boligportal.dk/find?placeIds=15&minRooms=3'
    myurl = 'https://www.boligportal.dk/find?placeIds=49%2C65%2C42896%2C365%2C16358%2C14&minRooms=3&minRentalPeriod=3'
    driver.implicitly_wait(15)
    driver.get(myurl)
    AdCards = driver.find_elements_by_css_selector('div.CardList.AdCardWrapper')
    mysource = driver.page_source

    #Apply beutifulSoup
    soup = BeautifulSoup(mysource, features="lxml")

    #Extract complete apartment information
    bolig = soup.find_all('a', attrs={'class': 'AdCard'})
    url = []
    for u in bolig:
       url.append(u['href'])
    url = ['https://www.boligportal.dk' + s for s in url]

    #Extract specific tags
    title = soup.find_all('div', attrs={'class': 'AdCard__title'})
    location = soup.find_all('div', attrs={'class': 'AdCard__location'})
    price = soup.find_all('div', attrs={'class': 'AdCard__price'})
    description = soup.find_all('div', attrs={'class': 'AdCard__description'})
    dateAdded = soup.find_all('div', attrs={'class': 'AdCard__date'})

    # Generates unique ids for apartments
    ids = []
    for i in range(21):
        j = str(uuid.uuid1())
        ids.append(j)

    df = pd.DataFrame(data={'id': ids,
                            'title': [t.text for t in title],
                            'location': [l.text for l in location],
                            'price': [p.text for p in price],
                            'description': [d.text for d in description],
                            'link': [u for u in url]})

    return df.iloc[3:]

#df.to_csv('testDf.csv')

#if __name__ == '__main__':
#    scrape()