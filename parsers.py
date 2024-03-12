from bs4 import BeautifulSoup
import ParseExceptions as exc

def parse_index(page_content) -> list:
    soup = BeautifulSoup(page_content, "html.parser").body

    dropped_items = soup.find_all('a', class_ = "user-thumb") # finding last winner users` id
    winners_links = []


    for item in dropped_items:
        winners_links.append(f"{item['href']}")

    return winners_links

def parse_user_page(page_content) -> str:
    if(check_if_limited(page_content) == True): raise exc.LimitedException("Rate has been limited")

    soup = BeautifulSoup(page_content, "html.parser").body

    try:
        user_steam_page = soup.find('a', class_="login")
        return user_steam_page['href']
    except AttributeError:
        raise exc.NotEnoughTimeException("Was not enough time to parse the url")
    except TypeError:
        raise exc.NotEnoughTimeException("Was not enough time to parse the url")

def check_if_limited(page_content) -> bool:
    title = BeautifulSoup(page_content, "html.parser").title

    try: 
        return title.get_text().find("denied") != -1
    except AttributeError:
        raise exc.NotEnoughTimeException("Was not enough time to parse the url")