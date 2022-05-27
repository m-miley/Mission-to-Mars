# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from pprint import pprint

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Setup HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

########### TITLE / SUBTITLE ###########

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

########### FEATURED IMAGES ###########

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

########### TABLE DATA ###########

# Use Panas read_html() to scrape entire table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description','Mars','Earth']
df.set_index('description', inplace=True)
df

# Live updates - convert to html for web presentation
df.to_html()

########### MARS HEMISPHERES ###########

# Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Create a list to hold the images and titles.
hemisphere_image_urls = []

# Write code to retrieve the image urls and titles for each hemisphere.

# locate image thumbnail and grab list of tags info
img_soups = img_soup.find_all('div', class_="item")

# iterate through tags
for img in img_soups:
    
    # grab url for full image 
    enhanced_url = url + img.find('a')['href']
    # visit url
    browser.visit(enhanced_url)
    html = browser.html
    img_soup2 = soup(html, 'html.parser')
    
    # visit tag and grab full url
    full_img_url = url + img_soup2.find('img', class_='wide-image').get('src')
    # visit tag and grab full title
    img_title = img_soup2.find('h2', class_='title').text
    
    # Create empty dict to hold url/title data
    hemispheres = {}
    
    # img_url = url + img.get('src')

    hemispheres['img_url'] = full_img_url
    hemispheres['title'] = img_title
    
    hemisphere_image_urls.append(hemispheres)

# Quit the browser
browser.quit()