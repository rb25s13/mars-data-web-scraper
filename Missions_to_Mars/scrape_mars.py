from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_dict = {}

    # get the latest news title and blurb
    homeurl = 'https://redplanetscience.com/'
    browser.visit(homeurl)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_dict['news_title']  = soup.find('div', class_='content_title').text
    mars_dict['news_p'] = soup.find('div', class_='article_teaser_body').text

    # get the latest featured image url
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_dict['featured_image_url'] = image_url + soup.find('img', class_='headerimage')['src']

    # get the table of mars facts
    facts_url = 'https://galaxyfacts-mars.com/'

    table = pd.read_html(facts_url)[0]
    new_header = table.iloc[0]
    table = table[1:]
    table.columns = new_header
    mars_dict['htmltable'] = table .to_html(classes='table table-striped')

    # Store data in a dictionary
    astr_url = 'https://marshemispheres.com/'
    browser.visit(astr_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemi = soup.find('div', class_='results')
    images = hemi.find_all('div', class_='description')

    url_list = []
    for image in images:
        img_url = image.find('a', class_='itemLink')['href']
        url_list.append(img_url)
    himg_urls = [astr_url + url for url in url_list]
    dl_list = []
    hemisphere_image_urls = []
    for himg_url in himg_urls:
        browser.visit(himg_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        # dl_div = soup.find('div', class_='downloads')
        # dl_link = dl_div.find_all('a')[1]['href']
        dl_link = soup.find('img', class_='wide-image')['src']
        dl_url = astr_url + dl_link
        title_div = soup.find('div', class_='cover')
        title = title_div.find('h2').text
        dl_list.append(dl_url)
        hemisphere_image_url = {"title": title, "img_url": dl_url}
        hemisphere_image_urls.append(hemisphere_image_url)
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    return mars_dict
