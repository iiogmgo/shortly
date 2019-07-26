## Shortly

![main](/shortly/static/shortly-1.png)
![urls](/shortly/static/shortly-2.png)

## Developement/Testing Env

### Developing Language

- Python 3.7

### Framework

- Flask

## Setup

1. install requirements

   `pip install -r requirements.txt`
   
2. Copy config.template.py to make config.py and fill in the contents.
   
3. init db

   `python db.py db init`
   
   `python db.py db migrate`
   
   `python db.py db upgrade`
   
4. run flask

   `flask run`