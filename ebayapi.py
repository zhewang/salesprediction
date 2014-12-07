import requests
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool
from urllib.parse import urlparse, parse_qs

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }

def GetSearchResults(keywords):
    kwd_str = '+'.join(keywords)

    response = requests.get('http://www.ebay.com/sch/i.html?_from=R40&_nkw='+kwd_str+'&_sacat=0&rt=nc&LH_BIN=1&_sop=12', headers=headers)
    soup = BeautifulSoup(response.text.encode('utf-8'))

    results = []
    for li in soup.find_all('li', id=re.compile(r"^item*")):
        results.append(li.find('a')['href'])

    return results

def GetSalesData(item_url, savePath):    
    response = requests.get(item_url, headers=headers)
    soup = BeautifulSoup(response.text.encode('utf-8'))

    sales_data = soup.find('a', href = re.compile(r'http://offer.ebay.com/ws/eBayISAPI.dll\?ViewBidsLogin/*'))

    if sales_data == None:
        print("No salse data.")
        # TODO save this info to file
    else:
        response = requests.get(sales_data['href'], headers=headers)
        soup = BeautifulSoup(response.text.encode('utf-8'))
        sales_list = soup.find_all('tr', attrs={"bgcolor":  re.compile(r"^(#ffffff|#f2f2f2)$")})

        o = urlparse(sales_data['href'])
        p_dict = parse_qs(o.query)
        # print(p_dict['item'][0])
        
        saveFile = open(savePath+'/'+p_dict['item'][0]+'.txt','w')

        for record in sales_list:
            saveFile.write(record.find_all('td')[3].text+" "+record.find_all('td')[4].text+'\n')

def SearchEbay(keywords, savePath):
    item_urls = GetSearchResults(keywords)

    # GetSalesData(item_urls[0])
    # Sequential
    for url in item_urls:
        GetSalesData(url, savePath)

    # parallel
    # pool = Pool(10)
    # pool.map_async(GetSalesData, item_urls)
    # pool.close()
    # pool.join()

if __name__ == '__main__':
    keywords = ['olay']
    SearchEbay(keywords, './')

    
   