

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# set up the URL for scraping
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
# **executable_path is unpacking the dictionary we've stored the path in
browser = Browser('chrome', **executable_path)


#we'll assign the url and instruct the browser to visit it.
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
# we're searching for elements with a specific combination of tag (ul and li) and attribute (item_list and slide, respectively)
#we're also telling our browser to wait one second before searching for components.
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


#set up the HTML parser:
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')




# After searching for the HTML components you'll use to identify the title and paragraph you want
#Begin scraping
#The specific data is in a <div /> with a class of 'content_title'
slide_elem.find("div", class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


#There are two methods used to find tags and attributes with BeautifulSoup:

#.find() is used when we want only the first class and attribute we've specified.
#.find_all() is used when we want to retrieve all of the tags and attributes.


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p
0


# ### Featured Images

#Let's start getting our code ready to automate all of the clicks to get the image we want
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()



# Find the more info button and click that

#method to search for an element that has the provided text
#wait_time allows the browser to fully load before we search for the element
browser.is_element_present_by_text('more info', wait_time=1)
#This method will take our string ‘more info’ to find the link associated with the "more info" text.
more_info_elem = browser.links.find_by_partial_text('more info')
#tell Splinter to click that link
more_info_elem.click()

#browser will navigate to the next page.



# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')



# Find the relative image url
# "This is where the image we want lives—use the link that's inside these tags."
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel



# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url



#scrape the entire table with Pandas'
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df

df.to_html()


#the code is designed to grab the most recent data, so if it's run at a later time, all of the results will have been updated

#ends session
browser.quit()

# ##  Adjust the current web app to include all four of the hemisphere images- challenge

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# In[20]:

# Path to chromedriver
get_ipython().system('which chromedriver')


# set up the URL for scraping
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
# **executable_path is unpacking the dictionary we've stored the path in
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)



# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


slide_elem.find("div", class_='content_title')



# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title



# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image
# 



# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()



# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')



# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel



# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()



df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df

df.to_html()


# ### Mars Weather


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)

# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')

# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)



# 2. Create a list to hold the images and titles.
hemisphere_image_urls = ['image_url:','title:']


# 3. Write code to retrieve the image urls and titles for each hemisphere.

#test
#browser.links.find_by_partial_text('Enhanced')

#scraping 1st title
Enhanced = browser.links.find_by_partial_text('Cerberus').click()
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_url_1 = img_soup.select_one('img.wide-image').get("src")
img_url_fin_1 = f'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mar{img_url_1}'

html = browser.html
news_soup = soup(html, 'html.parser')
slide_element = news_soup.select_one('div.content')
title_1= slide_element.find('h2',class_="title").get_text()
title_1



img_url_fin_1



#scraping 2nd title
Enhanced = browser.links.find_by_partial_text('Schiaparelli').click()
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_url_en = img_soup.select_one('img.wide-image').get("src")
img_url_fin_2 = f'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mar{img_url_en}'

html = browser.html
news_soup = soup(html, 'html.parser')
slide_element_2 = news_soup.select_one('div.content')
title_2= slide_element_2.find('h2',class_="title").get_text()
title_2


img_url_fin_2


#scraping 3rd title
Enhanced = browser.links.find_by_partial_text('Syrtis').click()
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_url_en = img_soup.select_one('img.wide-image').get("src")
img_url_fin_3 = f'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mar{img_url_en}'

html = browser.html
news_soup = soup(html, 'html.parser')
slide_element_3 = news_soup.select_one('div.content')
title_3= slide_element_3.find('h2',class_="title").get_text()
title_3


#scraping 4th title
Enhanced = browser.links.find_by_partial_text('Valles').click()
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_url_en = img_soup.select_one('img.wide-image').get("src")
img_url_fin_4 = f'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mar{img_url_en}'

html = browser.html
news_soup = soup(html, 'html.parser')
slide_element_4 = news_soup.select_one('div.content')
title_4= slide_element_4.find('h2',class_="title").get_text()
title_4




img_url = [img_url_fin_1, img_url_fin_2, img_url_fin_3, img_url_fin_4]
img_url


title = [title_1, title_2, title_3, title_4]
title



hemisphere_image_urls = [{img_url[i]:title[i] for i in range(len(img_url))}]


## 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()






