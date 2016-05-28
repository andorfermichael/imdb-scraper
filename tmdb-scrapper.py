from imdbpie import Imdb
import json

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('iso-8859-1')

MAX_ITERATIONS = 9

imdb = Imdb(anonymize=True) # to proxy requests

def gen_json(movies):
    with open('movies.json', mode='w') as moviesjson:
        json.dump(movies, moviesjson)

def do_query(id):
        actors = list()
        writers = list()
        directors = list()
        genres = list()

        print("tt" + "%06d" % (0,) + str(id))
        movie = imdb.get_title_by_id("tt000000" + str(id))

        for person in movie.credits:
            if person.token == 'directors':
                directors.append(person.name)
            elif person.token == 'writers':
                writers.append(person.name)
            else:
                actors.append(person.name)

        for genre in movie.genres:
                genres.append(genre)

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


if __name__ == "__main__":
    with open('movies.json', mode='w') as moviesjson:
        json.dump({'movies': []}, moviesjson)

    movies = {'movies': []}

    for i in range(1, MAX_ITERATIONS):
        movie = do_query(i)

        movies["movies"].append(movie)

        gen_json(movies)