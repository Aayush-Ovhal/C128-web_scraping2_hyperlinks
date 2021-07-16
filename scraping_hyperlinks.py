from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time 
import csv

headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink"]
planet_data = []
new_planet_data = []

start_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"

browser = webdriver.Chrome("C:/Users/Aayush/Downloads/chromedriver_win32/chromedriver.exe")

browser.get(start_url)

time.sleep(10)

def scrape():
     for i in range(0, 443):
          soup = BeautifulSoup(browser.page_source, "html.parser")
          for ul_tag in soup.find_all("ul", attrs = {"class", "exoplanet"}):
              li_tags = ul_tag.find_all("li")
              temp_list = []
              for index, li_tag in enumerate(li_tags):
                   if index == 0:
                        temp_list.append(li_tag.find_all("a")[0].contents[0])
                   else:
                        try: 
                            temp_list.append(li_tag.contents[0])
                        except:
                             temp_list.append("")  

              planet_data.append(temp_list) 
              hyperlink_li_tag = li_tags[0]
              temp_list.append("https://exoplanets.nasa.gov/" + hyperlink_li_tag.find_all("a", href = True) [0]["href"])
              planet_data.append(temp_list)
          browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

def scrape_for_data(hyperlink):
     page = requests.get(hyperlink)
     soup_list = BeautifulSoup(page.content, "html.parser")
     temp_list = []
     for tr_tag in soup_list.find_all("tr", attrs={"class:", "fact_row"}):
          td_tags = tr_tag.find_all("td")
          for td_tag in td_tags:
              try:
                  temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
              except:
                   temp_list.append("")
              new_planet_data.append(temp_list)

for index, data in enumerate(planet_data):
     scrape_for_data([5])

final_planet_data = []

for index, data in enumerate(planet_data):
     final_planet_data.append(data + new_planet_data[index])

scrape()

with open("something.csv", "w") as f:
     csv_writer = csv.writer(f)
     csv_writer.writerow(headers)
     csv_writer.writerows(planet_data)