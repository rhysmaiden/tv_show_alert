import requests
from bs4 import BeautifulSoup
import sys
from inscriptis import get_text
import urllib.request
import time
import datetime
import os

def send_email():
  return True

def scrape_page(website,word_track):

  site= "http://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol=JPASSOCIAT&fromDate=1-JAN-2012&toDate=1-AUG-2012&datePeriod=unselected&hiddDwnld=true"
  hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8',
         'Connection': 'keep-alive'}

  req = urllib.request.Request(website,None,headers=hdr)
  html = urllib.request.urlopen(req).read().decode('utf-8')

  text = get_text(html)

  if word_track in text:
      return True
  else:
    return False


file = open("track.csv","r+")
updated_file = open("update.csv","w")

for f in file:
    print(f.split(","))
    website,word_track,episode,day,time,repeat,alerted = f.split(",")

    website = website.strip()
    episode = int(episode.strip())

    original_word_track = word_track
    word_track = word_track.strip() + str(episode).zfill(2)

    alerted = alerted.strip()

    current_day = datetime.datetime.now().strftime("%A")
    current_hour = int(datetime.datetime.now().strftime("%H"))

    if alerted == 'False':

      if current_day == day and int(time) >= current_hour:
        
        print("Looking at site...")
        if scrape_page(website,word_track):
          send_email()
          episode += 1
          alerted = "True"

    else:
      yesterday = datetime.date.today() - datetime.timedelta(days=1)
      yesterday = yesterday.strftime("%A")

      if day == yesterday:
        alerted = "False"

    updated_file.write(website + "," + original_word_track + "," + str(episode) + "," + day + "," + time + "," + repeat + "," + alerted)
    
os.rename('update.csv','track.csv')
    

    

    
