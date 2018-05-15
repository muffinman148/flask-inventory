# Flask-Inventory Project
## Overview
Many companies perform inventory counts on a monthly basis. This is primarily conducted by one or more employee’s to cultivate a number of inventory stock left after the previous inventory period. Some companies opt to record inventory as it is used, while others will adopt the approach of recording inventory for a given period. Our goal as a software team is develop a product that will allow a company to record inventory on a monthly basis with high efficiency and accuracy. We would like to eliminate as much human error as possible by offloading the counting method off onto a scale and computer. We believe that this would best be achieved through the use of low cost technology, such as: Raspberry Pi, scale and barcode reader. We can implement a system that will quickly identify a product and using previously recorded weights provide an accurate count. 

## Background
This is a project for CSUSM's CS 441 Software Engineering class.

## Setup
Download assets.
```sh
$ git clone https://github.com/muffinman148/flask-inventory
$ cd flask-inventory
$ virtualenv venv
$ source venv/bin/activate 
```

Create ``password.py`` file for your ``config.py`` with your own database information.
```python
import os

# This file should never be on git.
import os

KEY = os.environ.get('SECRET_KEY') or 'random-key-here'
DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://username:password@host/database'
```

Run the site.
```sh
+(venv) $ flask run -h 0.0.0.0
```

## Features
- [X] Login
- [X] User Administration
- [X] Label Printing (with Brother QL-720NW)
- [ ] Scale Reading (Partially working)

## Resources
* [Flask](http://flask.pocoo.org/)
* [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* [Scale (hx711 and loadcell)](https://github.com/tatobari/hx711py)

## Special Thanks
* Miguel Grinberg is a talented individual that really provided a significant amount of help with creating the flask website
* Professor Ye for all of his lessons throughout the semester
