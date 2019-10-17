
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)   

def scrape():
    browser = Browser('chrome', headless=False)
    con = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(con)
    db = client.MarsMission_db
    data = db.info
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    paragraphs = []
    for x in range(2):
        html = browser.html
        soup = bs(html, 'html.parser')
        information = soup.find_all(class_='slide')
        for info in information:
            title = info.find(class_='content_title').text
            body = info.find(class_ ='article_teaser_body').text
            titles.append(title)
            paragraphs.append(body)
    first_article = titles[0]
    print(first_article)
    first_paragraph = paragraphs[0]
    print(first_paragraph)
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    image = browser.html
    soup = bs(image, 'html.parser')
    image_url = soup.find('img', class_="thumb")['src']
    featured_image_url = "https://www.jpl.nasa.gov/" + image_url
    print(featured_image_url)
    browser.visit('https://twitter.com/marswxreport?lang=en')
    tweet = soup.find(class_="TweetTextSize--normal").text
    replace_n = tweet.replace('\n',', ')
    mars_weather_tweet = replace_n.replace('hPapic.twitter.com/2moNAouxXa','')
    print(mars_weather_tweet)
    browser.visit('https://space-facts.com/mars/')
    table_url = 'https://space-facts.com/mars/'
    table = pd.read_html(table_url)
    table_df = table[1]
    table_df.columns=['Description', 'Value']
    table_df.set_index('Description', inplace = True)
    html_table = table_df.to_html()
    mars_table_html_string = html_table.replace('\n','')
    table_df.to_html('Mars_Table.html')
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    html = browser.html
    soup = bs(html,'html.parser')

    results = soup.find('div', class_='result-list')
    hemi_info = results.find_all('div', class_='item')

    hemi_titles = []
    hemi_image_urls_dict = []

    for hemi in hemi_info:
        title = hemi.find('h3').text
        hemi_titles.append(title)
        url_to_hemi = hemi.find('a')['href']
        full_url = "https://astrogeology.usgs.gov/" + url_to_hemi
        #hemi_image_urls.append(full_url)
        browser.visit(full_url)
        html = browser.html
        soup = bs(html,'html.parser')
        find_image = soup.find('div', class_ ='downloads')
        actual_hemi_url = find_image.find('a')['href']
        #replaced_image_url_1 = actual_hemi_url.replace('[<a href=', '')
        #fully_replaced_image_url = replaced_image_url_1.replace(' target="_blank">Sample</a>','')
        hemi_image_urls_dict.append({"Title": title,"img_url": actual_hemi_url})

    return hemi_image_urls_dict
    
    
