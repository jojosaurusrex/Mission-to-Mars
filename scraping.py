#!/usr/bin/env python
# coding: utf-8

# In[13]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hem_data(browser) 
    #I think this using hem_data function in order to define the variable

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "List_of_imgs_titles": hemisphere_image_urls
    }
    # Stop webdriver and return data
    browser.quit()
    return data


# In[3]:

def mars_news(browser):

    # Visit the mars nasa news site / Scrape Mars News
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # elements with a specific combination of tag (div) and attribute 
    #(list_text). Also telling it to wait

    # In[4]:

    html = browser.html #using splinter initially
    news_soup = soup(html, 'html.parser') #using beautifulSoup for the rest
   
    try:
        slide_elem = news_soup.select_one('div.list_text') 
        #does this only allow to select a singular value? if so, it makes sense

        # CSS works from right to left, so when using select_one, the first 
        #matching element is the actually the last one?

        #word for word from module
        # the first matching element returned will be a <li /> element with a 
        #class of slide and all nested elements within it.

        # In[5]:

        # slide_elem.find('div', class_='content_title')

        # In[6]:

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # news_title

        # In[7]:

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        # news_p

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

# In[8]:

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # In[9]:


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # In[10]:


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


    # In[11]:

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # In[12]:


    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url 


# In[14]:

def mars_facts():

    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
      return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html(classes="table table-striped")

def hem_data(browser):
    #define the website we are visiting
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # delay for loading the page
    #browser.is_element_present_by_css('div.list_text', wait_time=1)

    #define beautiful soup to parse through html code
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    #scrape hemisphere data /UNSURE IF I NEED TO CHANGE VARIABLES
    hemisphere_image_urls = []
    thumbnails = browser.find_by_css('a.product-item img')

    for image in range(len(thumbnails)):
        hemispheres = {}

        browser.find_by_css('a.product-item img')[image].click()

        full = browser.links.find_by_text('Sample').first
        hemispheres['image_url'] = full['href']

        title = browser.find_by_css("h2.title").text
        hemispheres['title'] = title

        hemisphere_image_urls.append(hemispheres)

        browser.back()
    #return scraped data as a list of dictionairies w/URL string anf title of each hemisphere image
    return hemisphere_image_urls

# In[16]:


# df.to_html()
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())



# In[17]:


# browser.quit()


# In[ ]:




