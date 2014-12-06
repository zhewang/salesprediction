import requests
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }

def GetSearchResults(keywords):
    kwd_str = '+'.join(keywords)

    response = requests.get('http://www.ebay.com/sch/i.html?_nkw='+kwd_str+'&_sacat=0&rt=nc&LH_BIN=1', headers=headers)
    soup = BeautifulSoup(response.text.encode('utf-8'))

    viewer = soup.find(id='ListViewInner')
    results = []

    if viewer != None:
        for li in viewer.find_all('li', class_='sresult lvresult clearfix li'):
            # print(li.find('a')['href'])
            results.append(li.find('a')['href'])

    return results

def GetSalesPage(item_url):    
    response = requests.get(item_url, headers=headers)
    soup = BeautifulSoup(response.text.encode('utf-8'))

    sales_data = soup.find('a', href = re.compile(r'http://offer.ebay.com/ws/eBayISAPI.dll\?ViewBidsLogin/*'))

    print(item_url)
    if sales_data == None:
        print("No salse data.")
    else:
        GetSalesData(sales_data['href'])

def GetSalesData(sales_url):
    response = requests.get(sales_url, headers=headers)
    soup = BeautifulSoup(response.text.encode('utf-8'))
    sales_list = soup.find_all('tr', attrs={"bgcolor":  re.compile(r"^(#ffffff|#f2f2f2)$")})

    print(len(sales_list))

if __name__ == '__main__':
    keywords = ['apple','iphone','5s']

    # for item in GetSearchResults(keywords):
        # print(item)

    item_urls = GetSearchResults(keywords)

    pool = Pool(10)
    pool.map_async(GetSalesPage, item_urls)
    pool.close()
    pool.join()
   