# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 15:57:51 2017

@author: prajila
"""

import requests
from bs4 import BeautifulSoup
import re, csv
from datetime import datetime, timedelta

page = requests.get("https://www.eia.gov/dnav/ng/hist/rngwhhdm.htm")
soup = BeautifulSoup(page.content, 'html.parser')

links = []
for a in soup.find_all('a', class_="NavChunk"):
    links.append(a['href'])
    
firstlink = "https://www.eia.gov/dnav/ng/hist/"
dailylink = firstlink + links[0]
weeklylink = firstlink + links[1]
monthlylink = firstlink + links[2]
annuallink = firstlink + links[3]

#daily
dailypage = requests.get(dailylink)
dailysoup = BeautifulSoup(dailypage.content, 'html.parser')

table = dailysoup.find('table', summary="Henry Hub Natural Gas Spot Price (Dollars per Million Btu)")
with open('gas_price_daily.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Price'])
    
    for row in table.find_all('tr')[1:]:
        col = row.find_all('td')
        dailydate = (col[0].text).split("to",1)[0]
        if dailydate == "":
            pass
        else:
            year = re.findall(r"(\d{4})", dailydate)[0]
            month = re.findall("[a-zA-Z]+", dailydate)[0]
            date = dailydate.split("-",1)[1].strip()
            dailydate = year + "-" + month + "-" + date
            startdate = datetime.strptime(dailydate,'%Y-%b-%d').date()
            for i in range(5):
                date = startdate + timedelta(days=i)
                price = col[i+1].text
                writer.writerow([date, price])
                
#weekly
weeklypage = requests.get(weeklylink)
weeklysoup = BeautifulSoup(weeklypage.content, 'html.parser')

table = weeklysoup.find('table', summary="Henry Hub Natural Gas Spot Price (Dollars per Million Btu)")
with open('gas_price_weekly.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Price'])
    for row in table.find_all('tr')[2:]:
        startyear = row.find('td', class_="B6")
        if startyear is not None:
            year = startyear.text.strip()
            if year != "" and year[0] in '0123456789':    
                year = re.findall(r"(\d{4})", year)[0]
                datecol = row.find_all('td', class_="B5")
                pricecol = row.find_all('td', class_="B3")
                for i in range(5):
                    date = datecol[i].text.strip()
                    if date:
                        finaldate = year + "/" + date
                        date = datetime.strptime(finaldate,'%Y/%m/%d').date()
                    else:
                        finaldate = ""
                    price = pricecol[i].text
                    writer.writerow([finaldate, price])

#monthly
monthlypage = requests.get(monthlylink)
monthlysoup = BeautifulSoup(monthlypage.content, 'html.parser')

table = monthlysoup.find('table', summary="Henry Hub Natural Gas Spot Price (Dollars per Million Btu)")
with open('gas_price_monthly.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Price'])
    for row in table.find_all('tr')[1:]:
        col = row.find_all('td')
        startyear = (col[0].text).strip()
        if startyear != "" and startyear[0] in '0123456789': 
            for i in range(1, 13):
                date = startyear + "-" + str(i) + "-" + "01"
                date = datetime.strptime(date,'%Y-%m-%d').date()
                price = col[i].text
                writer.writerow([date, price])
        else:
            pass
    
#annual
annualpage = requests.get(annuallink)
annualsoup = BeautifulSoup(annualpage.content, 'html.parser')

table = annualsoup.find('table', summary="Henry Hub Natural Gas Spot Price (Dollars per Million Btu)")
with open('gas_price_annual.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Price'])
    
    for row in table.find_all('tr')[1:]:
        col = row.find_all('td')
        startyear = (col[0].text).strip()
        if startyear != "" and startyear[0] in '0123456789':  
            startyear = re.findall(r"(\d{4})", startyear)[0]
            for i in range(10):
                year = int(startyear) + i
                date = str(year) + "-" + "01" + "-" + "01"
                date = datetime.strptime(date,'%Y-%m-%d').date()   
                price = col[i+1].text
                writer.writerow([date, price])
        else:
            pass
   