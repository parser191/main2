from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from SETTINGS import RESULT_FILE_TXT_NAME, HOW_MANY_SITES_TO_WINNER_LIST, INTERM_LINKS_TXT

import time
from datetime import datetime

from parsers import parse_user_page
from driver_manager import create_proxified_driver

import ParseExceptions as exc

driver = create_proxified_driver()

def form_winners(last_read, how_many_to_read = HOW_MANY_SITES_TO_WINNER_LIST) -> tuple[list, int]:
    winners = []
    try:
        with open(f"{INTERM_LINKS_TXT}", 'r') as read:
            while((len(winners) <= how_many_to_read)):
                line = read.readline()
                if(line == ''): break
                line = line.split('|')

                if(int(line[0]) < last_read):
                    pass
                else:
                    winners.append(line[1])
                    last_read += 1
    except FileNotFoundError:
        open(f"{INTERM_LINKS_TXT}", "w").close()
    return (winners, last_read)

not_enough_time_list = []
last_read = 0


while(True):

    # newDriverNeeded = False

    (winners, last_read) = form_winners(last_read)
    winners = winners + not_enough_time_list
    not_enough_time_list.clear()
    if(winners == []): time.sleep(10)
    parsing_counter = 0

    result_list = []

    time_start = time.time()
    for win in winners:
        try:
            driver.get(win)
        except TimeoutException:
            print(f"Time Out on user {win}")
        except WebDriverException:
            print("Probably page crashed or too long connection time. Creating a new driver...")
            driver.quit()
            driver = create_proxified_driver()

        try:
            parse_res = parse_user_page(driver.page_source)
            parsing_counter += 1
            print(f"Parsed {parsing_counter}: {parse_res}")
            result_list.append(parse_res)
            
        except exc.NotEnoughTimeException:
            print(f"Not enough time for user {win}")
            not_enough_time_list.append(win)
        except exc.LimitedException:
            print("Rate has been limited. Creating new proxy...")
            driver.quit()
            driver = create_proxified_driver()
        except WebDriverException:
            print("Probably page crashed or too long connection time. Creating a new driver...")
            driver.quit()
            driver = create_proxified_driver()

        if(len(not_enough_time_list) >= 10):
            print("The site is trying to block connection or connection is to slow. Choosing different proxy.")
            driver.quit()
            driver = create_proxified_driver()
            winners = winners + not_enough_time_list
            not_enough_time_list.clear()

    time_end = time.time()
    print(f"Parsed {parsing_counter} accounts in {time_end - time_start} seconds")

    with open(f"{RESULT_FILE_TXT_NAME}", "a") as res:
        for elem in result_list:
            res.write(f"{elem}\n")
        res.close()



        