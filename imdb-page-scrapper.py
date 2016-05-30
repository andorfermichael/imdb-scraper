import argcomplete
import argparse
import json
import logging
import sys
import urllib2
from bs4 import BeautifulSoup

# Generates a movie json
def gen_json(movies):
    with open('movies.json', mode='w') as moviesjson:
        json.dump(movies, moviesjson)

# Requests the IMDb data for a given movie id
def process_page(url):

    # Retrieve html and setup parser
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, 'html.parser')

    # Process all table rows
    for tr in soup.find_all('tr'):
        try:
            # Parse single movie information
            id = tr.find('td', attrs={'class': 'title'}).find('a')['href'][8:-1]
            title = tr.find('td', attrs={'class': 'title'}).find('a').contents[0]
            year = tr.find('td', attrs={'class': 'title'}).find('span', attrs={'class': 'year_type'}).string[1:-1]
            outline = tr.find('td', attrs={'class': 'title'}).find('span', attrs={'class': 'outline'}).string
            director = tr.find('td', attrs={'class': 'title'}).find('span', attrs={'class': 'credit'}).find('a').contents[0]
            certificate = tr.find('td', attrs={'class': 'title'}).find('span', attrs={'class': 'certificate'}).find('span')['title']
            runtime = tr.find('td', attrs={'class': 'title'}).find('span', attrs={'class': 'runtime'}).string

            image_url = tr.find('td', attrs={'class': 'image'}).find('a').find('img')['src'][:-27] + '._V1_UX182_CR0, 0, 182, 268AL_.jpg'

            # Parse actors
            actors = list()
            actors_temp = tr.find('td', attrs={'class': 'title'}).find('span', attrs={'class': 'credit'}).find_all('a')
            for i, a in enumerate(actors_temp):
                if i != 0:
                    actors.append(actors_temp[i].contents[0])

            # Parse genres
            genres = list()
            genres_temp = tr.find('td', attrs={'class': 'title'}).find('span', attrs={'class': 'genre'}).find_all('a')
            for i, a in enumerate(genres_temp):
                genres.append(genres_temp[i].contents[0])

            # Store the movie data in a dictionary
            movie = {
                "actor": actors,
                "certification": certificate,
                "director": director,
                "genre": genres,
                "id": id,
                "title": title,
                "outline": outline,
                "image_url": image_url,
                "runtime": runtime,
                "year": year
            }

            # Append the movie data dictionary to the movies dictionary
            movies['movies'].append(movie)

            # Store the update movies dictionary in the json file (after each request)
            if args.storing == 'save':
                gen_json(movies)
                logger.info('Movie with id ' + id + ' stored in "movies.json".')
        except:
            continue

# Removes the wrapping dictionary of the data in the json file
def clean_json():
    # Load the dictionary from json file
    with open('movies.json') as f:
        movies = json.load(f)

    # Get the value of the wrapping dictionary
    movies_temp = movies['movies']

    # Store the unwrapped dictionaries
    with open('movies.json', mode='w') as moviesjson:
        json.dump(movies_temp, moviesjson)

# Main
if __name__ == '__main__':
    # Reload does the trick!
    reload(sys)

    # Set default encoding
    sys.setdefaultencoding('utf-8')

    # Define commandline arguments
    parser = argparse.ArgumentParser(description='scrape feature movies from IMDB''s "Most Voted Feature Films" list' , usage='python imdb-page-scrapper.py 10000 save')
    parser.add_argument('number', type=int, help='number of movies to request')
    parser.add_argument('storing', choices=['save', 'unsave'],
                        help='[save] store movies data after each request,[unsave] store movies data after all requests were executed')
    parser.add_argument('--start', type=int, help='the ranking number to start with')
    parser.add_argument('--overwrite', default='yes', choices=['yes', 'no'], help='[yes] overwrite json file, [no] append json file')
    args = parser.parse_args()

    if args.number < 0 or args.number % 50 != 0:
        parser.error('number has to be 50 or a multiple of 50 (e.g. 100, 250, 1500)')

    if args.start != None and (args.start < 0 or args.start % 50 != 0):
        parser.error('--start has to be 1, 50 or a multiple of 50 (e.g. 100, 250, 1500)')

    argcomplete.autocomplete(parser)

    # Set up a specific logger with desired output level
    logging.basicConfig(filename='./logs/imdb-page-scrapper.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logging.getLogger().addHandler(logging.StreamHandler())

    # Only show warnings for urllib2 library
    logging.getLogger('urllib2').setLevel(logging.WARNING)

    if args.start != None:
        START_ID = args.start
    else:
        START_ID = 0

    MAX_ITERATIONS = args.number

    if args.overwrite == 'yes':
        # Create a clean json file
        logger.info('JSON file "movies.json" created.')
        with open('movies.json', mode='w') as moviesjson:
            json.dump({'movies': []}, moviesjson)

        # Create a dictionary for the movies
        movies = {'movies': []}
    else:
        # Load the dictionary from json file
        with open('movies.json') as f:
            movies_temp = json.load(f)

        # Create a dictionary for the movies
        movies = {'movies': []}

        # Load data from file into created movies dictionary
        for i in range(0, len(movies_temp)):
            movies['movies'].append(movies_temp[i])

    # Process N films of IMDb
    logger.info('Movie retrieval started.')
    for i in range(START_ID, MAX_ITERATIONS / 50):
        # Calculate pagination
        pagination = START_ID + 1

        # Define url
        url = 'http://www.imdb.com/search/title?sort=num_votes&start=' + str(pagination) + '&title_type=feature'
        logger.info('Started scrapping of ' + url + '.')

        # Process page of 50 movies
        movie = process_page(url)
        logger.info('Finished scrapping of ' + url + '.')

    # Store the updated movies dictionary in the json file (after all movies were retrieved)
    if args.storing == 'unsave':
        gen_json(movies)
        logger.info('All retrieved movies were stored in "movies.json".')

    # Remove the wrapping dictionary
    clean_json()
    logger.info('"movies.json" cleaned up.')

logger.info('Movie retrieval finished.')