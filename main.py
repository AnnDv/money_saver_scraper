import requests, json, os
from bs4 import BeautifulSoup
from selenium import webdriver

option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

class product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def to_dict(self):
        return {"name": self.name, "price": self.price}

def scrapPandashop():
    productsList = []
    productCount = 0

    currentPage = 1

    while True:
        siteUrl = 'https://www.pandashop.md/ru/catalog/electronics/telephones/mobile/?page_=page_'+str(currentPage)
        page = requests.get(siteUrl)
        soup = BeautifulSoup(page.content, 'html.parser')

        nameAttribute = {'class': 'card-title'}
        priceAttribute = {'class': 'card-price_curr'}

        names = soup.findAll(attrs = nameAttribute)
        prices = soup.findAll(attrs = priceAttribute)

        for productNames in names:
            phoneName = productNames.text.removeprefix('Мобильный телефон').strip()
            productsList.append(product(phoneName, prices[productCount].text.removesuffix('лей').replace(' ','')))
            productCount+=1
        
        if not soup.find('a', attrs='btn-showmore'):
            break
        else:
            currentPage +=1
            productCount =0

    results = [product.to_dict() for product in productsList]
    results.sort(key=lambda obj: obj["price"])

    print('Scrapped products: '+str(len(productsList)))

    with open('Products_Pandashop.json', 'w', encoding='utf-8') as json_file:
        json.dump({"Pandashop": results}, json_file, indent=4, sort_keys=True)

def scrapRozetka():
    productsList = []
    productCount = 0
    currentPage = 1

    browser = webdriver.Chrome(chrome_options=option)
    while True:
        browser.get("https://rozetka.md/mobile-phones/c80003/page="+str(currentPage))
        content = browser.page_source
        soup = BeautifulSoup(content, 'html.parser')

        nameAttribute = {'class': 'g-i-tile-i-title'}
        priceAttribute = {'class': 'g-price-uah'}

        names = soup.findAll(attrs = nameAttribute)
        prices = soup.findAll(attrs = priceAttribute)

        for productNames in names:
            phoneName = productNames.text.strip().removeprefix('Мобильный телефон').strip()
            productsList.append(product(phoneName, prices[productCount].text.removesuffix("MDL").replace(' ', '').strip()))
            productCount+=1
        
        if not soup.find('a', attrs='g-i-more-link'):
            break
        else:
            currentPage +=1
            productCount =0

    browser.quit()

    results = [product.to_dict() for product in productsList]
    results.sort(key=lambda obj: obj["price"])

    print('Scrapped products: '+str(len(productsList)))

    with open('Products_Rozetka.json', 'w', encoding='utf-8') as json_file:
        json.dump({"Rozetka": results}, json_file, indent=4, sort_keys=True, ensure_ascii=False)

def scrapCactus():
    productsList = []
    productCount = 0

    currentPage = 1

    while True:
        siteUrl = 'https://www.cactus.md/ru/catalogue/electronice/telefone/smartphones/?sort_=ByView_Descending&page_=page_'+str(currentPage)
        page = requests.get(siteUrl)
        soup = BeautifulSoup(page.content, 'html.parser')

        nameAttribute = {'class': 'catalog__pill__text__title'}
        priceAttribute = {'class': 'catalog__pill__controls__price'}

        names = soup.findAll(attrs = nameAttribute)
        prices = soup.findAll(attrs = priceAttribute)

        for productNames in names:
            phoneName = productNames.text.strip()
            productsList.append(product(phoneName, prices[productCount].text.removesuffix('лей').replace(' ','')))
            productCount+=1
        
        if not soup.find('button', attrs='pull-left'):
            break
        else:
            currentPage +=1
            productCount =0

    results = [product.to_dict() for product in productsList]
    results.sort(key=lambda obj: obj["price"])

    print('Scrapped products: '+str(len(productsList)))

    with open('Products_Cactus.json', 'w', encoding='utf-8') as json_file:
        json.dump({"Cactus": results}, json_file, indent=4, sort_keys=True)

def scrapSelection(val):
    clear = lambda: os.system('cls')
    clear()
    print('\nScraping Started. Please wait...')
    if val == '1':
        scrapPandashop()
    elif val == '2':
        scrapRozetka()
    elif val == '3':
        scrapCactus()
    else:
        print('Wrong number, try again!')
        return
    print('Ready! Check .json in same folder where main.py located!')

print("Money Saver Scraper by Piotr Shishkov")
print("Using Beautiful Soup 4")
while True:
    print("\n______________________________________")
    print('1. Get Products from Pandashop.MD')
    print('2. Get Products from Rozetka.MD')
    print('3. Get Products from Cactus.MD')
    print('4. Exit')
    print("______________________________________")
    val = input('Select option: ')
    
    if val == '4':
        break
    scrapSelection(val)
