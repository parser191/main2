from selenium.common.exceptions import TimeoutException
import time
from parsers import parse_index
from driver_manager import create_driver

from SETTINGS import INTERM_LINKS_TXT

def check_duplicates(str_list: list, filename) -> list:
    no_dups = []
    all_lines = []

    try:
        with open("im_links.txt", 'r') as file:
            line = file.readline()
            while line:
                all_lines.append(line.split('|')[1])
                line = file.readline()
            file.close()
    except FileNotFoundError:
        print("File hasn`t been created yet")

    print("All lines in file: ")
    print(all_lines)

    for string in str_list:
        if((f"{string}\n" not in all_lines)):
            if(string not in no_dups):
                no_dups.append(string)
        else:
            print(f"{string} is already in file")

    return no_dups

open(f"{INTERM_LINKS_TXT}", "w").close()
index_url = "https://case-battle.win"

driver = create_driver(True, 5.0)

try:
    driver.get(index_url)
except TimeoutException:
    print("Time Out on page")

time.sleep(10)
counter = 0

while(True):
    winners = parse_index(driver.page_source)
    print(winners)
    check_dup = []

    for i in range(len(winners)):
        formed_str = f"{index_url}/{winners[i][1:]}"
        check_dup.append(formed_str)

    check_dup = check_duplicates(check_dup, f"{INTERM_LINKS_TXT}")
    print(check_dup)


    with open(f"{INTERM_LINKS_TXT}", "a") as file:
        for string in check_dup:
            file.write(f"{counter}|{string}\n")
            counter+=1
        file.close()
    time.sleep(1)