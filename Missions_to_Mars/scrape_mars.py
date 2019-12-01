from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

    # Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_par = article.find("div", class_ ="article_teaser_body").text
    mars_data["mars_news"] = news_title
    mars_data["mars_paragraph"] = news_par

    # JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]
    url = 'https://www.jpl.nasa.gov'
    mars_image = (url)+(image)
    mars_data["mars_image"] = mars_image


    # Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_data["mars_weather"] = p.text


    # Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    html_table = df.to_html()   
    mars_data["mars_facts"] = html_table

    # Mars hemisheres
    hemisphere_image_urls = []
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    for item in items:
        title = item.find('h3').text
        href = item.find('a')['href']
        url = 'https://astrogeology.usgs.gov'
        link = (url)+(href)
        browser.visit(link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('a',target='_blank')['href']
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

    mars_data["mars_hemisphere"] = hemisphere_image_urls

    return mars_data

scrape
print("it worked")