# Star Wars characters explorer

## SW API
https://swapi.co/api/people/ is down but I found an alternative https://swapi.dev/api/

In case it's not 100% compatible some changes need to be made to the etl
code (data_operations.py file) and possibly to API client. 

## Value count note
It wasn't clear from the requirements whether the Value Count is about the full dataset 
or just the displayed items (with possible use of Load more). 
I decided to use it on the full dataset.

## Installation

Wick docker-compose

```bash
docker-compose build
docker-compose run app python manage.py migrate
docker-compose up
```

or on host machine - requires database and configuration changes

```bash
pip install poetry
poetry install
python manage.py migrate
python manage.py runserver
```

## Possible improvements
- tests!!!
- configuration is hardcoded in settings.py - it should be injected from external source
- there is no styling on frontend - it could use some minimal Bootstrap
- breadcrumbs for easier navigation would be nice
- handling selected headers for Value Count is currently tricky and should be improved
 
 ## Efficiency improvements
- fetching all of planets could be replaced by fetching only the ones we need (especially
if set of planets is way larger than characters)
 - hash join could be faster/more memory efficient than normal one
 - `petl.appendcsv` can be used to deal with saving large dataset
 - some other method could be used to read limited number of lines from csv
