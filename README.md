# Rest API report of a race with converting and storing data to the database

---


## Requirements

  * Python 3.10

## Local development requirements

Application is using flake8, isort, mypy and black code checkers alongside pre-commit 
hooks for verifying code before each commit

    $ pip install pipenv
    $ pipenv install
    $ pre-commit install

To check manually use 

    $ pre-commit run --all-files

## Quickstart

To initialize database setup environmental variables 
- 'DB_PATH' with path to database file to store
- 'DATA_PATH' with racing data files:
  - abbreviations.txt - lines formatted 'abbreviation_driver name_driver team'
  - end.log & start.log - lines formatted 'abbreviation%Y-%m-%d_%H:%M:%S.%f '

and use next scripts:


    $ python create_db_tables.py
    $ python fill_db_tables.py

*File 'example.db' in 'db' folder can be used as a reference for required database schema.

To run an application:


    $ python main.py

## License
[MIT](https://choosealicense.com/licenses/mit/)