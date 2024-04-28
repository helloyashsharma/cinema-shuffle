# cinema-shuffle

Work in progress python script to pick movies based on user criteria. This product uses the TMDB API but is not endorsed or certified by TMDB.


## Features

- Bearer token validation
- List upcoming movies
- Specify year range, multiple genres, rating range and language to search for movies
- Use and edit local config file for movie search parameters


## Requirements
 1. TMDB api bearer token - Can be obtained from your TMDB account at https://www.themoviedb.org/
 
 2. `requests` python library to send requests to the tmdb api.


## Run Locally

Clone the project

```bash
  git clone https://github.com/helloyashsharma/cinema-shuffle.git
```

Go to the project directory

```bash
  cd cinema-shuffle
```

Install dependencies

```python
  pip install requests
```

Run the program

```python
  python cinema-shuffle.py
```

