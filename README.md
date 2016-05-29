# IMDb Scrapper

```IMDb Scrapper``` stores a given number of movies from the Internet Movie Database as JSON.


## Requirements

- python 2.7


## Installation & Setup
Download and install required libs and data:
```bash
pip install imdbpie
```


## Usage
Collect and store the first 10,000 movies from the IMDb:
```python
python imdb-scrapper.py 10000 save
```

Collect and store the movies 15,000 to 25,000 from the IMDb:
```python
python imdb-scrapper.py --start 15000 10000 save
```

Collect and store the movies 30,000 to 35,000 from the IMDb and append them to the existing data in the movies.json:
```python
python imdb-scrapper.py --start 30000 5000 --overwrite no save
```