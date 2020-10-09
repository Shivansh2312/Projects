import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import tqdm

def get_soup(url):
    try:
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text,'html.parser')
            return soup
        else:
            print("page error",page.status_code)
            return None
    except:
        print("Internet error")
        return None

def number_of_product(soup):
    product = soup.find_all('div',{'class':'_2kSfQ4'})
    if len(product)>0:
        print('Number of products '+str(len(product))+" \n")
        return product
    else:
        print("no Products found")
        return None

def extract_details(product):
        name = item.find('div',{'class':'iUmrbN'}).text
        
        offer = item.find('div',{'class':'BXlZdc'}).text
        
        try:
            description = item.find('div',{'class':'_3o3r66'}).text
        except Exception as e:
            description = ' '
        
        link = item.find('a',{'class':'K6IBc-'}).attrs.get('href')
        
        return{
            'Name':name,
            'Offer':offer,
            'Description':description,
            'Link':'https://www.flipkart.com'+link
        }

if __name__ == '__main__':
    data = []
    weburl = input("Enter the url here:")
    bsoup = get_soup(weburl)
    no_of_product = number_of_product(bsoup)
    for item in no_of_product:
        detail = extract_details(item)
        data.append(detail)
    df = pd.DataFrame(data)
    current_date = datetime.now()
    day = current_date.day
    month = current_date.month
    yr = current_date.year
    todays_date = str(day)+'-'+str(month)+'-'+str(yr)

    df.to_excel('Flipkart_offer_'+todays_date+'.xlsx')
    print('Offers Scraped and Saved Successfully')
else:
    print("Sorry Scrapping Closed")