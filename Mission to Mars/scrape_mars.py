#!/usr/bin/env python
# coding: utf-8


# converting your Jupyter notebook into a Python script called `scrape_mars.py`

# dependencies
from bs4 import BeautifulSoup 
from splinter import Browser, browser
import pandas as pd
import time
import requests
import re


def init_browser():
    executable_path = {'executable_path': 'C:/Users/vijay/Downloads/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()



    # Mars News
    # assign url; use browser to 'get' url
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)

    time.sleep(1)

    # create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Use .find to locate the "div" and "class" and return only text
    news_title = soup.find('div', class_= 'content_title')

    news_p = soup.find('div', class_= 'article_teaser_body')

    # print text to confirm 
    print(news_title.text)
    print(news_p.text)

    # Mars image
    # assign url; use browser to 'get' url
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)

    time.sleep(1)

    # create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    image = soup.find('img', class_= 'fancybox-image')
    footer = soup.find("footer")
    link = footer.find('a')

    # assign the url string to a variable called `featured_image_url`.
    featured_image_url = link['data-fancybox-href']

    # save a complete url string for this image
    print('https://www.jpl.nasa.gov/' + featured_image_url)

    # Mars weather
    # assign url; use browser to 'get' url
    url_mars_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_mars_weather)

    time.sleep(1)

    # create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # using regular expressions .compile function
    mars_weather = re.compile(r'sol')
    mars_weather = soup.find('span', text = mars_weather).text 
    print(mars_weather)

    # Mars facts
    # assign url; use browser to 'get' url
    url_facts = "https://space-facts.com/mars/"
    browser.visit(url_facts)

    time.sleep(1)

    # create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # making a get request 
    response = requests.get(url_facts)

    # scrape the table data from 'table' and 'id' elements
    mars_facts = soup.find('table', id ="tablepress-p-mars-no-2").text
    print(mars_facts)

    # Mars table data
    table = pd.read_html(url_facts)
    table

    df = table[0]
    html_table = df.to_html()
    html_table

    df.to_html('table.html')

    # Mars Hemisphere
    # assign url; use browser to 'get' url
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)

    time.sleep(1)

    # create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # variable to locate the 'div' with 'item' from url
    items = soup.find_all('div', class_= 'item')

    # create an empty list to store results
    url_hemisphere_img = []

    # set variable to visit main url 
    main_url = 'https://astrogeology.usgs.gov'

    # create a for loop 
    for i in items:
        
        # locate titles
        title = i.find('h3').text
        
        # locate first partial img_url
        partial_img_url = i.find('a', class_= 'itemLink product-item')['href']
        
        # return to main_url; then partial img url
        browser.visit(main_url + partial_img_url)
        
        # initiate new html browser
        partial_img_html = browser.html
        
        # use beautiful soup and splinter to scrape each page
        soup = BeautifulSoup(partial_img_html, 'html.parser')
        
        # set variable to find full 'img' & 'src' urls
        img_url = main_url + soup.find('img', class_='wide-image')['src']
        
        # append titles and imgs; return as a list of dictionaries
        url_hemisphere_img.append({"title": title, "img_url": img_url})
        
    url_hemisphere_img

    # Close the browser after scraping
    browser.quit()

    # Store data in a dictionary
    mars_info = {
            "News Title": news_title,
            "News Paragraph": news_p,
            "Featured Image": featured_image_url,
            "Mars Weather": mars_weather,
            "Mars Facts": mars_facts,
            "Mars Table": table,
            "Mars Hemisphere": url_hemisphere_img
        }


    # Return results
    return mars_info