import requests
from bs4 import BeautifulSoup as BS
import re
import sqlite3
import os

# SETTINGS
site = 'http://kinogo-net.org/ru/page/'
poster_path = '/image/film_app/posters/'  # example /image/film_app/posters/Одесскийпароход_1578227511-553214192.jpg
screen_path = '/image/film_app/screens/'


# time decorator
def get_time(func):
    import time
    # start = time.time() # in this case time for all functions is summarized

    def wrapper(*args, **kwargs):
        start = time.time()
        response = func(*args, **kwargs)
        print(func.__name__, time.time() - start)
        return response

    return wrapper


""" PARSER """


# soup for url
def get_html_data(url: str) -> BS:
    response = requests.get(url)
    content = response.content.decode()
    soup = BS(content, "html.parser")
    return soup


# film list (urls) for one page
def get_film_list(soup: BS) -> []:
    tags = soup.findAll("div", {"class": "carou-inner pseudo-link"})
    films_links = [item['data-link'] for item in tags]
    return films_links


# parser for film details page
def get_film_details(url: str) -> {}:
    soup = get_html_data(url)
    kinogo_id = url.split('/')[4].strip('.html')

    title = soup.find("h1", {"class": "kino-h"}).text.split(' (')[0]

    # TODO: PROBLEM: site has changed format 09.04.2020
    # poster = 'http://kinogo-net.org' + \
    #          soup.find('div', {"class": "kino-desc full-text clearfix"}).findNext('img', {"itemprop": "image"})['src']
    poster = soup.find('div', {"class": "kino-desc full-text clearfix"}).findNext('img', {"itemprop": "image"})['src']

    # description
    try:
        description = soup.find('div', {"class": "kino-desc full-text clearfix"}). \
            findNext('span', {"itemprop": "description"}).text.split("\n")[2]
    except IndexError:
        description = ''

    # year, duration, genres
    try:
        tags = soup.find("ul", {"class": "kino-lines ignore-select margin-top"})
        genres = tags.find('div', text=re.compile('Жанр')).parent.text.split(': ')[1]
        duration = tags.find('div', text=re.compile('Продолжительность')).parent.text.split(': ')[1]
        year = tags.find('div', text=re.compile('Год выпуска')).parent.text.split(': ')[1]
    except Exception:
        year, duration, genres = '', '', ''

    # screens
    tags = soup.findAll("a", {"class": "highslide"})
    screens = [item['href'] for item in tags]

    film_details = {
        'kinogo_url': url,
        'kinogo_id': kinogo_id,  # TODO 1) remove url field and use id to identify already loaded films
        'title': title,
        'poster': poster,
        'description': description,
        'year': year,
        'duration': duration,
        'genres': genres,
        'screens': screens,
    }
    # print(film_details)
    return film_details


""" SAVE IMAGE FILES """


# Save posters and screens for film
# TODO split into separate functions - generate relative_path and save_file
def save_file(url: str, local_storage: str, title: str) -> str:
    MEDIA_DIR = '../media'
    fld = MEDIA_DIR + local_storage
    if not os.path.exists(fld):
        os.mkdir(fld)
    title = ''.join(e for e in title if e.isalnum())
    relative_path = local_storage + title + '_' + url.split('/')[-1]  # or url.split('/')[7]
    abs_path = MEDIA_DIR + relative_path
    if not os.path.exists(abs_path):  # allows not to rewrite existent files
        file = requests.get(url)
        with open(abs_path, 'wb') as temp:
            for chunk in file.iter_content(4096):  # 8192 bytes on 64-bit platform
                temp.write(chunk)
    return relative_path


""" INSERT INTO DB """


# TODO split into separate functions - get_conn, find_duplicates, insert_into, update_record
def update_db(film_details: {}):
    #  Prepare variables for statements
    title = film_details['title']
    poster = film_details['poster']
    description = film_details['description']
    description = description.replace('"', '')  # TODO fix  this crutch - problem on insert into DB
    kinogo_url = film_details['kinogo_url']
    year = film_details['year']
    duration = film_details['duration']
    genres = film_details['genres']
    screens = film_details['screens']

    film_db = r"../db.sqlite3"
    conn = sqlite3.connect(film_db)
    cursor = conn.cursor()

    # Already loaded films
    # TODO: use kinogo_id instead of kinogo_url to identify duplicates
    statement = f"""
    SELECT url, id from film_app_film WHERE url = "{kinogo_url}"
    """
    loaded_films = cursor.execute(statement).fetchall()

    if len(loaded_films) <= 0:  # WHY "if loaded_films.rowcount <= 0:" is not working? it returns (-1)
        # INSERT for film
        statement = f"""
        INSERT INTO film_app_film ("title", "url", "description", "poster", "duration", "year", "genres")
        VALUES (   "{title}", "{kinogo_url}", "{description}","{poster}", "{duration}", "{year}", "{genres}")"""
        cursor.execute(statement)

        # INSERT for film screenshots
        film_id_db = cursor.lastrowid
        statement = f"""
        INSERT INTO film_app_screenshots (film_id, screenshot)
        VALUES (?, ?)
        """
        for el in screens:
            film_screens = (film_id_db, el)
            cursor.execute(statement, film_screens)
    else:
        for el in loaded_films:
            if el[0] == kinogo_url:
                fid = el[1]
                # UPDATE for film
                statement = f"""
     UPDATE film_app_film
     SET "title" = "{title}", "url" = "{kinogo_url}", "description"="{description}",
         "poster"="{poster}", "duration"="{duration}", "year"="{year}", "genres"="{genres}"
     WHERE id = {fid}
    """
                cursor.execute(statement)
                # TODO: implement UPDATE for film screenshots, refactor (move to separate functions)

    conn.commit()
    conn.close()


@get_time
def generate_full_list(depth: int, start_page: int):
    all_films = []
    for page in range(start_page, start_page + depth):
        URL = site + str(page) + '/'
        SOUP = get_html_data(URL)
        FILMS = get_film_list(SOUP)
        for url in FILMS:
            film = get_film_details(url)
            all_films.append(film)
    #  TODO delete diagnostic code below
    print('===' * 20)
    for i in all_films:
        print(i['kinogo_id'])
    print(f'Films in list: {len(all_films)}')
    return all_films


@get_time
def save_all_images(all_films: dict):
    for film in all_films:
        try:
            #  save poster
            film['poster'] = save_file(film['poster'], poster_path, film['title'])
            #  save screens
            for screen in film['screens']:
                i = film['screens'].index(screen)
                film['screens'][i] = save_file(screen, screen_path, film['title'])
            # update_db(film)
        except requests.exceptions.ConnectionError:
            print(f'Connection error: {requests.exceptions.ConnectionError}', film)
            continue
    return all_films


@get_time
def save_all_into_db(all_films: dict):
    for film in all_films:
        try:
            update_db(film)
        except (Exception, sqlite3.OperationalError):
            print(f'DBError: {film}')
            continue


if __name__ == '__main__':
    lst = generate_full_list(depth=10, start_page=1)
    img = save_all_images(lst)
    db = save_all_into_db(lst)
