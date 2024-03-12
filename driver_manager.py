from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from SETTINGS import USER_PROXY_IP_TXT_FILE, PARSING_SITE_TIMEOUT, SHOW_BROWSER_WINDOW
import time
import random

def create_driver(headless: bool, timeout: float , proxy: str = "") -> webdriver:
    options = webdriver.ChromeOptions()
    if(headless): 
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--incognito")
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument("--disable-extensions")

    seleniumwire_options = {}

    if(proxy != ""):
        seleniumwire_options = {
            'proxy': {
                'http': f'http://{proxy}',
            }
        }   

    driver = webdriver.Chrome(options = options, seleniumwire_options=seleniumwire_options)
    
    driver.set_page_load_timeout(timeout)
    return driver

def choose_proxy() -> str:     
    proxies  = []
    with(open(USER_PROXY_IP_TXT_FILE, 'r')) as file:
        line = file.readline()
        while line:
            proxies.append(file.readline())
            line = file.readline()
    return random.choice(proxies)

def create_proxified_driver(headless: bool = not SHOW_BROWSER_WINDOW, timeout: float = PARSING_SITE_TIMEOUT) -> webdriver:

    
    proxy_is_active = False
    driver = None
    while(not proxy_is_active):
        proxy = choose_proxy()
        driver = create_driver(headless, 10, proxy)

        print("Checking proxy: " + proxy)
        try:
            driver.get("https://www.whatismyip.com")
            proxy_is_active = True
            print("Proxy has been chosen. IP: " + proxy)
        except TimeoutException:
            driver.quit()
            print("Not working, choosing different...")
        except WebDriverException:
            driver.quit()
            print("Driver went wrong, trying different ip...")


    driver.set_page_load_timeout(timeout)
    return driver