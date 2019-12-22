from bs4 import BeautifulSoup
import requests

# print(soup.prettify())



def getID(username):
    print(username)
    url = 'http://gettwitterid.com/?user_name=' + username + '&submit=GET+USER+ID'
    source = requests.get(url).text
    soup = BeautifulSoup(source,'lxml')
    info_container = soup.find('div',class_='info_container')
    # print(info_container.table.find_all('td')[1])
    twitter_id = info_container.table.find_all('td')[1].text
    return twitter_id
    # print(twitter_id)
    # for td in info_container.table.find_all('td'):
    #     print (td)


if __name__=='__main__':
    getID('RawalRuchit');

