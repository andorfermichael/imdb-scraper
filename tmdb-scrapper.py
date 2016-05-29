from imdbpie import Imdb
import json

import sys

# Reload does the trick!
reload(sys)
sys.setdefaultencoding('iso-8859-1')

MAX_ITERATIONS = 9

# Proxy the requests
imdb = Imdb(anonymize=True)

# Generates a movie json
def gen_json(movies):
    with open('movies.json', mode='w') as moviesjson:
        json.dump(movies, moviesjson)

# Requests the IMDB data for a given movie id
def do_query(id):

        # Create lists for fields which can have more than one feature
        actors = list()
        writers = list()
        directors = list()
        genres = list()

        print("tt" + "%06d" % (0,) + str(id))

        # Retrieve the movie as object
        movie = imdb.get_title_by_id("tt000000" + str(id))

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

        # Store the movie data in a dictionary
        movie_data = {
          "id": movie.imdb_id,
          "name": str(movie.title),
          "year": movie.year,
          "runtime": str(movie.runtime) + " min.",
          "plot": movie.plot_outline,
          "release_date": movie.release_date,
          "certification": movie.certification,
          "director": directors,
          "genre": genres,
          "actor": actors
        }

        return movie_data

# Removes the wrapping dictionary of the data in the json file
def clean_json():
    # Load the dictionary from json file
    with open('movies.json') as f:
        movies = json.load(f)

    # Get the value of the wrapping dictionary
    movies_temp = movies["movies"]

    # Store the unwrapped dictionaries
    with open('movies.json', mode='w') as moviesjson:
        json.dump(movies_temp, moviesjson)


# Main
if __name__ == "__main__":
    # Create a clean json file
    with open('movies.json', mode='w') as moviesjson:
        json.dump({'movies': []}, moviesjson)

    # Create a dictionary for the movie
    movies = {'movies': []}

    # Process N films of IMDB
    for i in range(1, MAX_ITERATIONS):
        # Get the movie data
        movie = do_query(i)

        # Append the movie data dictionary to the movies dictionary
        movies["movies"].append(movie)

        # Store the update movies dictionary in the json file
        gen_json(movies)

    # Remove the wrapping dictionary
    clean_json()