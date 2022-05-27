# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

####### MAIN FUNCTION ###########
# Initialize browser, Create data dict, End WebDriver, and Return scraped data
def scrape_all():
    # Initiate headless driver for deployment - Setup Splinter Driver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Implement mars_news() to scrape and gather title and paragraph text
    news_title, news_paragraph = mars_news(browser)

    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now(),
        'hemispheres': hemispheres(browser)
    }

    # Quite Driver and return data
    browser.quit()
    return data

###### TITLE / SUBTITLE ###########
def mars_news(browser):
    
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Setup HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    # Return news_title and news_p
    return news_title, news_p

##### FEATURED IMAGES ###########
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

########## TABLE DATA ###########
def mars_facts():
    try:
        # Use Panas read_html() to scrape entire table
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    
    # Assign columns and set index of pandas df
    df.columns=['description','Mars','Earth']
    df.set_index('description', inplace=True)

    # Return Live updates - convert to html for web presentation, add bootstrap
    return df.to_html(classes="table table-striped")

########## HEMISPHERES IMAGES ###########
def hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    hemisphere_image_urls = []
    
    img_soups = img_soup.find_all('div', class_="item")
    
    for img in img_soups:
        enhanced_url = url + img.find('a')['href']
        browser.visit(enhanced_url)
        html = browser.html
        img_soup2 = soup(html, 'html.parser')

        full_img_url = url + img_soup2.find('img', class_='wide-image').get('src')
        img_title = img_soup2.find('h2', class_='title').text
        
        hemispheres = {}
        hemispheres['img_url'] = full_img_url
        hemispheres['title'] = img_title
        hemisphere_image_urls.append(hemispheres)
    
    return hemisphere_image_urls

# If running locally, run program and print results
if __name__ == "__main__":
    print(scrape_all())