import requests
from bs4 import BeautifulSoup

def GetSearchResults(keywords):


    kwd_str = '+'.join(keywords)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }
    response = requests.get('http://www.ebay.com/sch/i.html?_nkw='+kwd_str+'&_sacat=0', headers=headers)

    soup = BeautifulSoup(response.text.encode('utf-8'))

    viewer = soup.find(id='ListViewInner')
    results = []
    for li in viewer.find_all('li', class_='sresult lvresult clearfix li'):
        # print(li.find('a')['href'])
        results.append(li.find('a')['href'])

    return results

if __name__ == '__main__':
    keywords = ['phone','apple']
    for item in GetSearchResults(keywords):
        print(item)