from selenium import webdriver
from selenium import common
import pandas as pd

# function for scraping hyperlinks
# function for parsing each hyperlink
# function for changing page
# function for wrapping all functions above

driver = webdriver.Chrome(r"C:\Users\tjunj\carelytics\jj\chromedriver.exe")

laz_url = "https://www.lazada.sg/skincare/?spm=a2o42.home.cate_4.1.654346b5rGbPg4"


def pdt_url_lst():
    """
    :return: extracts the urls of all products on the webpage as a string and stores them in a list
    """
    link_lst = []
    links = driver.find_elements_by_xpath('//div[@class="c16H9d"]/a')

    for link in links:
        link_attr = link.get_attribute('href')
        link_lst.append(link_attr)

    return link_lst


def merge_texts(webelements_lst):
    """
    :param webelements_lst: list of WebElements
    :return: extracts the text attribute from each element and joins the
    extracted texts into a single continuous list delimited
    """
    text_lst = []
    for element in webelements_lst:
        ele_text = element.text
        text_lst.append(ele_text)

    ', '.join(text_lst)

    return text_lst


def parse_pdt(pdt_url):

    # parses and extracts info of a single product

    driver.get(pdt_url)

    # basic product information
    try:
        name = driver.find_element_by_xpath('//div[@class="pdp-mod-product-badge-wrapper"]/span').text
    except common.exceptions.NoSuchElementException:
        name = 'NaN'
        pass

    try:
        price = driver.find_element_by_xpath('//div[@class="pdp-product-price"]/span').text
    except common.exceptions.NoSuchElementException:
        price = 'NaN'
        pass

    try:
        original_price = driver.find_element_by_xpath('//div[@class="origin-block"]/span').text
    except common.exceptions.NoSuchElementException:
        original_price = 'NaN'
        pass

    try:
        brand = driver.find_element_by_xpath('//div[@class="pdp-product-brand"]/a').text
    except common.exceptions.NoSuchElementException:
        brand = 'NaN'
        pass

    # delivery details

    try:
        delivery_option = driver.find_element_by_xpath('//*[contains(@class, "delivery-option-item '
                                                       'delivery-option-item_type_standard")]//div['
                                                       '@class="delivery-option-item__title"]').text
    except common.exceptions.NoSuchElementException:
        delivery_option = 'NaN'
        pass

    try:
        delivery_time = driver.find_element_by_xpath('//div[@class="delivery-option-item__time"]').text
    except common.exceptions.NoSuchElementException:
        delivery_time = 'NaN'
        pass

    try:
        delivery_fee = driver.find_element_by_xpath('//div[@class="delivery-option-item__shipping-fee"]').text
    except common.exceptions.NoSuchElementException:
        delivery_fee = 'NaN'
        pass

    try:
        delivery_extra = driver.find_element_by_xpath('//*[contains(@class, "delivery-option-item '
                                                      'delivery-option-item_type_normal")]//div['
                                                      '@class="delivery-option-item__title"]').text
    except common.exceptions.NoSuchElementException:
        delivery_extra = 'NaN'
        pass

    # return policies

    try:
        change_mind = driver.find_element_by_xpath('//div[@class="delivery-option-item__subtitle"]').text
    except common.exceptions.NoSuchElementException:
        change_mind = 'NaN'
        pass

    try:
        return_policy = driver.find_element_by_xpath('//*[contains(@class, "delivery-option-item '
                                                     'delivery-option-item_type_returnPolicy")]//div['
                                                     '@class="delivery-option-item__title"]').text
    except common.exceptions.NoSuchElementException:
        return_policy = 'NaN'
        pass

    # product details are presented as separate text bullet points and will be joined as a single string

    try:
        product_details_webelements = driver.find_elements_by_xpath(
            '//div[@class="html-content pdp-product-highlights"]//li')
        product_details = merge_texts(product_details_webelements)
    except common.exceptions.NoSuchElementException:
        product_details = 'NaN'
        pass

    # ratings

    try:
        ratings = driver.find_element_by_xpath('//span[@class="score-average"]').text
    except common.exceptions.NoSuchElementException:
        ratings = 'NaN'
        pass

    try:
        num_ratings = driver.find_element_by_xpath('//div[@class="count"]').text
    except common.exceptions.NoSuchElementException:
        num_ratings = 'NaN'
        pass

    values_lst = [name, price, original_price, brand, delivery_option, delivery_time, delivery_fee,
                  delivery_extra, change_mind, return_policy, product_details, ratings, num_ratings]

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

    headers = ['name', 'price', 'original_price', 'brand', 'delivery_option', 'delivery_time', 'delivery_fee',
               'delivery_extra', 'change_mind', 'return_policy', 'product_details', 'ratings', 'num_ratings']
    df = pd.DataFrame(val, columns=headers)

    return df


def parse_across_pages(url, page, threshold):

    # Process:
    # 1) scrape first page (pdt_url_lst(main url) -> parse_page) and save to dataframe
    # 2) scrape url of next page (next page url)
    # 3) scrape next page (pdt_url_lst(next page url) -> parse_page) and save to dataframe
    # 4) concat dataframe of the next page with the previous page
    # 5) repeat 2 and 3 until threshold reached and save final dataframe to csv file

    headers = ['name', 'price', 'original_price', 'brand', 'delivery_option', 'delivery_time', 'delivery_fee',
               'delivery_extra', 'change_mind', 'return_policy', 'product_details', 'ratings', 'num_ratings']
    data_df = pd.DataFrame(columns=headers)

    while page < threshold:
        driver.get(url)

        # scrape next page url
        next_page = driver.find_element_by_xpath(f'//li[@class="ant-pagination-item ant-pagination-item-{page + 1}"]/a')
        next_page_url = next_page.get_attribute('href')
        page = int(next_page.text)

        # scrape current page
        lst = pdt_url_lst()
        val_lst = parse_page(lst)
        page_df = page_dataframe(val_lst)

        # change to next page
        url = next_page_url

        # combine dataframes
        data_df = pd.concat([data_df, page_df])

    data_df.to_csv('sample.csv', index=False)

    return

parse_across_pages(laz_url, 1, 100)
