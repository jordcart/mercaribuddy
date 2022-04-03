import time
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver  # Import from seleniumwire

def get_token():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome("../chromedriver", chrome_options=options)

    driver.get('https://jp.mercari.com/search?keyword=realforce%20101')

    # sleep to let page finish loading
    time.sleep(5)

    # access requests via the `requests` attribute
    for request in driver.requests:
        if request.response:
            if request.url == "https://api.mercari.jp/v2/entities:search":
                # returning jwt token from making request
                return request.headers['dpop']
