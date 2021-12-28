import requests
from bs4 import BeautifulSoup
from twilio.rest import Client


def Handler(event=None, context=None):
    # Twilio setup
    account_sid = 'ACCOUNT SID GOES HERE'
    auth_token = 'AUTHORIZATION TOKEN GOES HERE'
    client = Client(account_sid, auth_token)

    # BeautifulSoup setup
    r = requests.get('https://www.svsound.com/collections/outlet-specials')
    content = r.content
    soup = BeautifulSoup(content, 'html.parser')

    # Search parameters and URL for SMS
    svs_url = 'https://svsound.com'
    search = 'PB-1000'
    outlet = 'Outlet'

    # Get all product cards from SVS outlet site and search using above parameters
    products = soup.find_all('div', class_='productCard_title')
    for item in products:
        current_item = item.h3.string
        if search in current_item and outlet in current_item and 'Pro' not in current_item:
            item_url = item.a.get('href')
            message_url = svs_url + item_url
            message = client.messages.create(
                body='Refurbished PB-1000 back in stock\n' + message_url,
                from_='+TWILIO NUMBER GOES HERE',
                to='+RECIPENT NUMBER GOES HERE'
            )
            return 0
        else:
            message = client.messages.create(
                body='PB-1000 still out of stock',
                from_='+TWILIO NUMBER GOES HERE',
                to='+RECIPIENT NUMBER GOES HERE'
            )
            return 1
