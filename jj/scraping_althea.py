from selenium import webdriver
from selenium import common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# function for scraping hyperlinks
# function for parsing each hyperlink
# function for changing page
# function for wrapping all functions above

driver = webdriver.Chrome(r"C:\Users\tjunj\carelytics\jj\chromedriver.exe")

sg_url = "https://sg.althea.kr/collections/skincare"
my_url = "https://my.althea.kr/collections/skincare"
ph_url = "https://ph.althea.kr/collections/skincare"
in_url = "https://in.althea.kr/collections/skincare"


def pdt_url_lst(driver):
    """
    :return: extracts the urls of all products on the webpage as a string and stores them in a list
    """
    link_lst = []
    links = driver.find_elements_by_xpath('//div[@class="ProductItem__Wrapper"]/a')

    for link in links:
        link_attr = link.get_attribute('href')
        link_lst.append(link_attr)

    return link_lst


def parse_pdt(pdt_url):
    # parses and extracts info of a single product

    driver.get(pdt_url)

    # basic product information
    try:
        name = driver.find_element_by_xpath('//div[@class="ProductMeta"]/h1').text
    except common.exceptions.NoSuchElementException:
        name = 'NaN'
        pass

    try:
        try:
            price = driver.find_element_by_xpath('//span[@class="ProductMeta__Price Price Text--subdued u-h4"]').text
            disc_price = 'NaN'
        except common.exceptions.NoSuchElementException:
            price = driver.find_element_by_xpath('//div[@class="ProductMeta__PriceList Heading"]/span[3]').text
            disc_price = driver.find_element_by_xpath('//div[@class="ProductMeta__PriceList Heading"]/span[2]').text
    except common.exceptions.NoSuchElementException:
        price = 'NaN'
        disc_price = 'NaN'
        pass

    try:
        try:
            brand = driver.find_element_by_xpath('//h2[@class="ProductMeta__Vendor Heading u-h6"]/a').text
        except common.exceptions.NoSuchElementException:
            brand = driver.find_element_by_xpath('//h2[@class="ProductMeta__Vendor Heading u-h6"]').text
    except common.exceptions.NoSuchElementException:
        brand = 'NaN'
        pass

    # Product details

    try:
        product_details = driver.find_element_by_xpath('//div[@id="ShortDescription"]/p').text
    except common.exceptions.NoSuchElementException:
        product_details = 'NaN'
        pass

    # Ratings

    try:
        ratings_web = driver.find_element_by_xpath('//span[@class="jdgm-prev-badge__stars"]')
        ratings = ratings_web.get_attribute('aria-label')
    except common.exceptions.NoSuchElementException:
        ratings = 'NaN'
        pass

    try:
        num_ratings = driver.find_element_by_xpath('//span[@class="jdgm-prev-badge__text"]').text
    except common.exceptions.NoSuchElementException:
        num_ratings = 'NaN'
        pass

    values_lst = [name, price, disc_price, brand, product_details, ratings, num_ratings]

    return values_lst


def parse_page(url_lst):
    # saves scraped info of all products on a single page into a compiled list

    all_pdt_val = []
    for url in url_lst:
        single_pdt_val = parse_pdt(url)
        all_pdt_val.append(single_pdt_val)

    return all_pdt_val


def page_dataframe(val):
    # saves extracted information from a single page into a dataframe

    headers = ['name', 'price', 'disc_price', 'brand', 'product_details', 'ratings', 'num_ratings']
    df = pd.DataFrame(val, columns=headers)

    return df


def parse_across_pages(url, page, threshold, countrycode):
    # country codes (str): 'sg', 'my', 'ph', 'in'

    # Process:
    # 1) scrape first page (pdt_url_lst(main url) -> parse_page) and save to dataframe
    # 2) scrape url of next page (next page url)
    # 3) scrape next page (pdt_url_lst(next page url) -> parse_page) and save to dataframe
    # 4) concat dataframe of the next page with the previous page
    # 5) repeat 2 and 3 until threshold reached and save final dataframe to csv file

    headers = ['name', 'price', 'disc_price', 'brand', 'product_details', 'ratings', 'num_ratings']

    data_df = pd.DataFrame(columns=headers)

    while page < threshold:
        driver.get(url)
        wait_page_load(driver)

        # scrape current page
        lst = pdt_url_lst(driver)
        val_lst = parse_page(lst)
        page_df = page_dataframe(val_lst)

        # change to next page
        url = f"https://{countrycode}.althea.kr/collections/skincare?page={page + 1}"

        # combine dataframes
        data_df = pd.concat([data_df, page_df])

        data_df.to_csv(f'althea_skincare_{countrycode}data{page}.csv', index=False)

        page += 1

    return


def wait_page_load(driver):
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, 'bc-sf-filter-load-more'))
        )

    return

# parse_across_pages(ph_url, 1, 24, 'ph')
parse_across_pages("https://ph.althea.kr/collections/skincare?page=17", 17, 24, 'ph')