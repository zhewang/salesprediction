import requests
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }

def GetSearchResults(keywords):
    kwd_str = '+'.join(keywords)

    response = requests.get('http://www.ebay.com/sch/i.html?_from=R40&_nkw='+kwd_str+'&_sacat=0&rt=nc&LH_BIN=1&_sop=12', headers=headers)
    # response = requests.get('http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&LH_BIN=1&_nkw=apple+iphone+5s&_sop=12', headers=headers)
    soup = BeautifulSoup(response.text.encode('utf-8'))

    temp = open("temp.html", 'wb')
    temp.write(response.text.encode('utf-8'))

    # viewer = soup.find(id='ListViewInner')
    # results = []

    # if viewer != None:
    #     for li in viewer.find_all('li', attrs={"_sp": "p2045573.m1686.l2058"}):
    #         # print(li.find('a')['href'])
    #         results.append(li.find('a')['href'])

    results = []
    for li in soup.find_all('li', id=re.compile(r"^item*")):
        results.append(li.find('a')['href'])

    return results

def GetSalesData(item_url):    
    response = requests.get(item_url, headers=headers)
    soup = BeautifulSoup(response.text.encode('utf-8'))

    sales_data = soup.find('a', href = re.compile(r'http://offer.ebay.com/ws/eBayISAPI.dll\?ViewBidsLogin/*'))

    if sales_data == None:
        print("No salse data.")
    else:
        response = requests.get(sales_data['href'], headers=headers)
        soup = BeautifulSoup(response.text.encode('utf-8'))
        sales_list = soup.find_all('tr', attrs={"bgcolor":  re.compile(r"^(#ffffff|#f2f2f2)$")})

        print(len(sales_list))

def SearchEbay(keywords):
    item_urls = GetSearchResults(keywords)

    # Sequential
    # for url in item_urls:
        # GetSalesData(url)

    # parallel
    pool = Pool(10)
    pool.map_async(GetSalesData, item_urls)
    pool.close()
    pool.join()

if __name__ == '__main__':
    keywords = ['olay']
    SearchEbay(keywords)

    
   