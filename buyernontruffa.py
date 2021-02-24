from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import time
import secrets

options = Options()
options.page_load_strategy = 'eager'


def purchase(username, password, item_url, cvv, country):
    if country == "Amazon.it":
        login_url = secrets.login_url_it
    elif country == "Amazon.es":
        login_url = secrets.login_url_es
    elif country == "Amazon.fr":
        login_url = secrets.login_url_fr
    elif country == "Amazon.de":
        login_url = secrets.login_url_de
    else:
        raise Exception("Error in link")

    address_xpath = '//*[@id="address-book-entry-0"]/div[2]/span/a'
    driver = webdriver.Chrome(os.getcwd()+"/chromedriver", options=options)

   # for logging into amazon
    driver.get(login_url)
    driver.find_element_by_xpath(
        '//*[@id="ap_email"]').send_keys(username + Keys.RETURN)
    driver.find_element_by_xpath(
        '//*[@id="ap_password"]').send_keys(password + Keys.RETURN)

    # end of login code
    time.sleep(0.1)
    # for getting into our product page
    driver.get(item_url)

    # once the button is activated ,click the buy now button
    driver.find_element_by_xpath(
        '//*[@id="buy-now-button"]').click()
    time.sleep(5)

    driver.switch_to.frame("turbo-checkout-iframe")
    driver.find_element_by_xpath('//*[@id="turbo-checkout-pyo-button"]').click()

    time.sleep(15)

purchase(secrets.email, secrets.password, 'https://www.amazon.fr/dp/B08MPRQR7L', secrets.ccv, "Amazon.fr")
