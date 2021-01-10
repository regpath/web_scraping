from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime

WEBDRIVER_PATH = r'C:\Users\Jeongyong\Documents\0_practice\chromedriver_win32\chromedriver'
def load_chrome_driver(show=False):
    options = webdriver.ChromeOptions() 
    if show == False:
        options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
    options.add_argument('--window-size=1920x1080')
    driver = webdriver.Chrome(WEBDRIVER_PATH, options=options)
    return(driver)
    
    def scrape_reviews(asin,allformats=True):
    p_num = 0
    driver = load_chrome_driver(show=True)
    reviews_df = pd.DataFrame()
    while True:
        p_num += 1
        url1 = 'https://www.amazon.com/product-reviews/' + asin + '/ref=cm_cr_arp_d_viewopt_srt?pageNumber=' + str(p_num) + '&sortBy=recent&'
        if allformats==True:
            url2 = url1 + 'all_formats'
        else:
            url2 = url1 + 'current_format'
        driver.get(url2)
        reviews_list = driver.find_elements_by_xpath("//div[@data-hook='review']")
        if len(reviews_list) == 0:
            print("Finished")
            break
        # if p_num == 1:
            # total_counts = driver.find_element_by_xpath("//span[@data-hook='cr-filter-info-review-count']").text.split(' ')[-2]
            # print('Total ' + str(total_counts) + ' reviews')
        if p_num%10 == 0:
            print(' Page {}'.format(p_num), end= ' ')
        for review1 in reviews_list:
            name1 = review1.find_element_by_xpath(".//span[@class='a-profile-name']").text
            # star1 = review1.find_element_by_xpath(".//div[@class='a-row']/a").get_attribute('title')
            star1 = review1.find_element_by_xpath(".//i[@data-hook='cmps-review-star-rating' or @data-hook='review-star-rating']").get_attribute('class')
            star1 = int(star1.split(' ')[2][-1])
            title1 = review1.find_element_by_xpath(".//*[@data-hook='review-title']").text
            date1 = review1.find_element_by_xpath(".//span[@data-hook='review-date']").text
            date1 = datetime.datetime.strptime(date1.split('on ')[1],'%B %d, %Y')
            format1 = review1.find_elements_by_xpath(".//a[@data-hook='format-strip']")
            if len(format1) == 0:
                format1 = ''
            else:
                format1 = format1[0].text
            purchased1 = review1.find_elements_by_xpath(".//span[@data-hook='avp-badge']")
            if len(purchased1) == 1:
                purchased2 = purchased1[0].text
            else:
                purchased2 = 'No'
            text1 = review1.find_element_by_xpath(".//span[@data-hook='review-body']").text
            noimg1 = len(review1.find_elements_by_xpath(".//div[@class='review-image-tile-section']/img"))
            helpful1 = review1.find_elements_by_xpath(".//span[@data-hook='helpful-vote-statement']")
            if len(helpful1) == 1:
                helpful2 = helpful1[0].text
            else:
                helpful2 = str(0)
            if len(review1.find_elements_by_xpath(".//span[@class='a-size-base']")) >= 1:
                nocomment1 = review1.find_element_by_xpath(".//span[@class='a-size-base']").text
            else:
                nocomment1 = 'No Comment'
            review_dict = {'name': name1,'rating': star1,'title': title1,'date': date1,'format': format1,'purchased': purchased2,
                                'text': text1,'no_images': noimg1,'helpful': helpful2,'no_comments': nocomment1}   
            reviews_df = reviews_df.append(review_dict, ignore_index=True)
    return reviews_df
    
# LG Gram 17" laptop
# Product Reviews URL: https://www.amazon.com/product-reviews/B082XQR86P
asins_lggram17 = 'B082XQR86P'

reviews_lggram17 = scrape_reviews(asins_lggram17)
