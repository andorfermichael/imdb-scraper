import argcomplete
import argparse
from imdbpie import Imdb
import json
import logging
import sys

# Generates a movie json
def gen_json(movies):
    with open('movies.json', mode='w') as moviesjson:
        json.dump(movies, moviesjson)

# Requests the IMDb data for a given movie id
def do_query(id):
        # Create lists for fields which can have more than one feature
        actors = list()
        writers = list()
        directors = list()
        genres = list()

        if imdb.title_exists('tt' + '%07d' % id) == False:
            following_id = id + 1
            logger.info('Movie with id tt' + '%07d' % id + ' does not exists. Continue with tt' + '%07d' % following_id)
            return False

        try:
            # Retrieve the movie as object
            movie = imdb.get_title_by_id('tt' + '%07d' % id)

            # Store the persons categorized by their positions
            for person in movie.credits:
                if person.token == 'directors':
                    directors.append(person.name)
                elif person.token == 'writers':
                    writers.append(person.name)
                else:
                    actors.append(person.name)

            # Store the genres
            for genre in movie.genres:
                    genres.append(genre)
        except TypeError:
            following_id = id + 1
            logger.info('Movie with id tt' + '%07d' % id + ' has inconsistent data. Continue with tt' + '%07d' % following_id)
            return False
        except:
            logger.info('An error occured while processing movie with id tt' + '%07d' % id + '. Continue with tt' + '%07d' % following_id)
            return False

        # Store the movie data in a dictionary
        movie_data = {
            "actor": actors,
            "certification": movie.certification,
            "director": directors,
            "genre": genres,
            "id": movie.imdb_id,
            "name": str(movie.title),
            "plot": movie.plot_outline,
            "poster_url": movie.poster_url,
            "cover_url": movie.cover_url,
            "release_date": movie.release_date,
            "runtime": str(movie.runtime) + ' min.',
            "year": movie.year
        }

        logger.info('Movie with id ' + movie.imdb_id + ' retrieved.')

        return movie_data

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
    parser = argparse.ArgumentParser(description='retrieve films from IMDB', usage='python imdb-scrapper.py 10000 save')
    parser.add_argument('number', type=int, help='number of movies to request')
    parser.add_argument('storing', choices=['save', 'unsave'],
                        help='[save] store movies data after each request,[unsave] store movies data after all requests were executed')
    args = parser.parse_args()

    argcomplete.autocomplete(parser)

    # Set up a specific logger with desired output level
    logging.basicConfig(filename='./logs/imdb-scrapper.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logging.getLogger().addHandler(logging.StreamHandler())

    # Only show warnings for request library
    logging.getLogger('requests').setLevel(logging.WARNING)

    MAX_ITERATIONS = args.number

    # Proxy the requests
    imdb = Imdb(anonymize=True)

    # Create a clean json file
    logger.info('JSON file "movies.json" created.')
    with open('movies.json', mode='w') as moviesjson:
        json.dump({'movies': []}, moviesjson)

    # Create a dictionary for the movie
    movies = {'movies': []}

    # Process N films of IMDb
    logger.info('Movie retrieval started.')
    for i in range(1, MAX_ITERATIONS + 1):
        # Get the movie data
        movie = do_query(i)

        if movie == False:
            continue

        # Append the movie data dictionary to the movies dictionary
        movies['movies'].append(movie)

        # Store the update movies dictionary in the json file (after each request)
        if args.storing == 'save':
            gen_json(movies)
            logger.info('Movie with id ' + movie['id'] + ' stored in "movies.json".')

    # Store the update movies dictionary in the json file (after all movies were retrieved)
    if args.storing == 'unsave':
        gen_json(movies)
        logger.info('All retrieved movies were stored in "movies.json".')

    # Remove the wrapping dictionary
    clean_json()
    logger.info('"movies.json" cleaned up.')

logger.info('Movie retrieval finished.')