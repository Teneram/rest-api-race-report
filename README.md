Core: 
[![Python](https://img.shields.io/badge/python-3.10-green?logo=python)](https://www.python.org/downloads/release/python-3100/)
[![Flask](https://img.shields.io/badge/Flask-2.2.3-blue.svg?logo=flask)](https://flask.palletsprojects.com/en/2.2.x/)
![REST API](https://img.shields.io/badge/REST%20API-Active-brightgreen)
[![Swagger](https://img.shields.io/badge/Swagger-OpenAPI-blue.svg?logo=swagger)](https://swagger.io/)
[![Pipenv](https://img.shields.io/badge/Pipenv-installed-blue?style=flat-square)](https://pypi.org/project/pipenv/)

Code style:
[![Flake8](https://img.shields.io/badge/flake8-6.0.0-red.svg)](https://flake8.pycqa.org/en/6.0.0/)
[![mypy](https://img.shields.io/badge/mypy-1.0.1-blue.svg)](https://mypy.readthedocs.io/en/stable/getting_started.html)
[![isort](https://img.shields.io/badge/isort-5.12.0-green.svg)](https://pypi.org/project/isort/)
[![Black Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/getting_started.html)


---

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