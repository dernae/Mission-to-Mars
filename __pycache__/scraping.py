
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt


#set up the URL for scraping
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
#driver = webdriver.Chrome(executable_path='C:/path/to/chromedriver.exe')
browser = Browser('chrome', **executable_path)



#When we add the word "browser" to our function, we're telling Python that we'll be using the browser variable we defined outside the function
def mars_news(browser):
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
    

        # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # After searching for the HTML components you'll use to identify the title and paragraph you want
        #Begin scraping
        #The specific data is in a <div /> with a class of 'content_title'
        #slide_elem.find("div", class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        #There are two methods used to find tags and attributes with BeautifulSoup:

        #.find() is used when we want only the first class and attribute we've specified.
        #.find_all() is used when we want to retrieve all of the tags and attributes.


        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        
    except AttributeError:
        return None, None
    return news_title, news_p
def scrape_all():
    # Initiate headless driver for deployment
    #headless= True allows scraping to happen behind the scenes rather than live
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    
    news_title, news_paragraph = mars_news(browser)  
    hemisphere_image_urls = hemisphere_data(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_image_urls": hemisphere_image_urls

    }

    # Stop webdriver and return data
    browser.quit()
    #browser.get(url)
    return data
# ### Featured Images

#Let's start getting our code ready to automate all of the clicks to get the image we want
def featured_image(browser):
    # Visit URL
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
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
    # Add try/except for error handling
    try:

        # Find the relative image url
        # "This is where the image we want lives—use the link that's inside these tags."
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        #scrape the entire table with Pandas'
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere_data(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = ['image_url:','title:']
    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    #test
    #browser.links.find_by_partial_text('Enhanced')

    #scraping 1st image
    Enhanced = browser.links.find_by_partial_text('Cerberus').click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_url_1 = img_soup.select_one('img.wide-image').get("src")
    img_url_fin_1 = f'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mar{img_url_1}'
    #scraping 1st title
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_element = news_soup.select_one('div.content')
    title_1= slide_element.find('h2',class_="title").get_text()

    #scraping 2nd image
    Enhanced = browser.links.find_by_partial_text('Schiaparelli').click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_url_en = img_soup.select_one('img.wide-image').get("src")
    img_url_fin_2 = f'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mar{img_url_en}'
    #scraping 2nd title
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_element_2 = news_soup.select_one('div.content')
    title_2= slide_element_2.find('h2',class_="title").get_text()
   
    #scraping 3rd image
    Enhanced = browser.links.find_by_partial_text('Syrtis').click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_url_en = img_soup.select_one('img.wide-image').get("src")
    img_url_fin_3 = f'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mar{img_url_en}'
    #scraping 3rd title
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_element_3 = news_soup.select_one('div.content')
    title_3= slide_element_3.find('h2',class_="title").get_text()


    #scraping 4th image
    Enhanced = browser.links.find_by_partial_text('Valles').click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_url_en = img_soup.select_one('img.wide-image').get("src")
    img_url_fin_4 = f'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mar{img_url_en}'
    #scraping 4th title
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_element_4 = news_soup.select_one('div.content')
    title_4= slide_element_4.find('h2',class_="title").get_text()

    #create list to hold all titles
    img_url = [img_url_fin_1, img_url_fin_2, img_url_fin_3, img_url_fin_4]

    #create list to hold all titles
    title = [title_1, title_2, title_3, title_4]
    #updating dictionary to hold titles and urls 
    hemisphere_image_urls = [{img_url[i]:title[i] for i in range(len(img_url))}]


    ## 4. Print the list that holds the dictionary of each image url and title.
    #hemisphere_image_urls


    # 5. Quit the browser
    browser.quit()

    #return the scraped data as a list of dictionaries with the URL string and title of each hemisphere image.
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())