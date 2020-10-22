from bs4 import BeautifulSoup


with open("test2.html") as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

#Extract the necessary information on apartments
bolig = soup.find_all('a', href =True, attrs={'class': 'AdCard'})
url = []
for u in bolig:
    url.append(u['href'])

title = soup.find_all('div', attrs = {'class': 'AdCard__title'})
location = soup.find_all('div', attrs={'class': 'AdCard__location'})
price = soup.find_all('div', attrs={'class': 'AdCard__price'})
description = soup.find_all('div', attrs={'class': 'AdCard__description'})
dateAdded = soup.find_all('div', attrs={'class': 'AdCard__date'})

#TODO figure out what is the best way to store the data. Maybe class or dataframe?

#Combine into one nice string

output = []
for i in range(0,len(url)):
    o = f'Title : {title[i].text}\nLocation: {location[i].text}\nPrice: {price[i].text}\nDate added: {dateAdded[i].text}\nURL:{url[i]}'
    output.append(o)
test = f'Title : {title[4].text}\nLocation: {location[4].text}\nPrice: {price[4].text}\nDate added: {dateAdded[4].text}\nURL:{url[4]}'
print(output[0])

print(soup.prettify())