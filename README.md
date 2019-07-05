# Flask-Inventory Project
## Overview
Many companies perform inventory counts on a monthly basis. This is primarily conducted by one or more employee’s to cultivate a number of inventory stock left after the previous inventory period. Some companies opt to record inventory as it is used, while others will adopt the approach of recording inventory for a given period. Our goal as a software team is develop a product that will allow a company to record inventory on a monthly basis with high efficiency and accuracy. We would like to eliminate as much human error as possible by offloading the counting method off onto a scale and computer. We believe that this would best be achieved through the use of low cost technology, such as: Raspberry Pi, scale and barcode reader. We can implement a system that will quickly identify a product and using previously recorded weights provide an accurate count. 

## Background
This is a project for CSUSM's CS 441 Software Engineering class. I will be continuing development through the summer.

## Setup

### Python 3.6.5
Pyenv setup for Python 3.6.5. [For more information on pyenv-installer.](https://github.com/pyenv/pyenv-installer)
```sh
$ curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
$ pyenv update
$ pyenv install 3.6.5
```

If you are having build issues check [here](https://github.com/pyenv/pyenv/wiki/common-build-problems) for fixes. Here is the fix for Ubuntu/Debian
```sh
$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
  xz-utils tk-dev
```

### Inventory System

Download assets.
```sh
$ git clone https://github.com/muffinman148/flask-inventory
$ cd flask-inventory
```

If you have pyenv installed:
```sh
$ pyenv local 3.6.5
```

Initialize virtualenv for the first time
```sh
$ python3 -m venv venv3
$ source venv3/bin/activate 
$ pip install -r requirements.txt
```

Otherwise, to start a virtualenv instance run:
```sh
$ source venv3/bin/activate
```

Run the ``startup.py`` to input information relating to:
* FLASK_APP (Flask App environment variable)
* FLASK_ENV (Flask production or development mode variable)
* SECRET_KEY (Secret key assigned to all sessions)
* SQLALCHEMY_DATABASE_URI (Database engine connection composed of 'sql-variant://username:password@hostname/database')
* ADMINS (Admin email)

Note: This will create ``.env`` and ``.flaskenv`` that dotenv will hook into.

### Database Setup

The following commands will initialize the database adding all tables.
```sh
flask db init
flask db migrate -m "All tables"
flask db upgrade
```

### Running the Site

Run the site.
```sh
+(venv3) $ flask run -h 0.0.0.0
```

## Features
- [X] Login
- [X] User Administration
- [X] Label Printing (with Brother QL-720NW)
- [X] Scale Reading (Partially working)

## Resources
* [Flask](http://flask.pocoo.org/)
* [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* [Scale (hx711 and loadcell)](https://github.com/tatobari/hx711py)

## Special Thanks
* Miguel Grinberg is a talented individual that really provided a significant amount of help with creating the flask website
* Professor Ye for all of his lessons throughout the semester
