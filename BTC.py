""" Show current BTC price from bitcoin.co.th & Line bot alert """
import requests, time, json, urllib.parse, datetime
from bs4 import BeautifulSoup
def main(start = 0):
    """ Call Function price() """
    price(start)

def line_sent(price):
    """
    sent message to line
    when BTC price change
    """
    now = datetime.datetime.now()
    LINE_ACCESS_TOKEN = " " # Line Token
    url = "https://notify-api.line.me/api/notify"
    print("[%02i:%02i:%02i] Price Change : Send Message" % (now.hour, now.minute, now.second))
    message = "[%02i:%02i:%02i] Now BTC Price : %s" % (now.hour, now.minute, now.second, price)
    msg = urllib.parse.urlencode({"message":message})
    LINE_HEADERS = {'Content-Type':'application/x-www-form-urlencoded',"Authorization":"Bearer "+LINE_ACCESS_TOKEN}
    session = requests.Session()
    send = session.post(url, headers=LINE_HEADERS, data=msg)
    print("[%02i:%02i:%02i] " % (now.hour, now.minute, now.second), end="")
    print(send.text)

def price(temp):
    """
    pull BTC price from bitcoin.co.th and display
    auto refresh 30 second
    """
    now = datetime.datetime.now()
    r = requests.get("https://bitcoin.co.th/")
    soup = BeautifulSoup(r.content, "html.parser")
    data = soup.find_all("div", {"class": "price"})
    print("[%02i:%02i:%02i] Now BTC Price : " % (now.hour, now.minute, now.second), end="")
    for i in range(len(data)):
        price = (data[i].text)
    print(price)
    if price != temp: # Price Change
        line_sent(price)
    temp = price
    time.sleep(30) # Delay 30 second
    main(temp) # call function main for loop

main()
