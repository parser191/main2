from driver_manager import create_driver
from parsers import parse_index, check_if_limited
import time
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

driver = create_driver(True, 10)

try:
    driver.get("https://case-battle.win")
except TimeoutException:
    print("Time Out on page")
time.sleep(10)

res = parse_index(driver.page_source)
if res == []:
    print(check_if_limited(driver.page_source))
    if(not check_if_limited(driver.page_source)):
        print(BeautifulSoup(driver.page_source).title)

print(res)