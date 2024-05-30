# Noordervliet-ShoppingList

This is a simple webapplication using python Flask run on the local host. In the application one can create an account and login to that account to save lists of their pantry staples and add these and other items to a shopping list. Shopping list items can be checked and will automatically be placed back into the pantry staple list if they are a staple.  

## Files 
Static files: contain the javascript and css__
Template files: contain the html for the different pages
Forms: contains the forms for signup and login
Main: defines the application in a function
Models: contains the model classes for users, staples, and groceries to be stored in a database
Routes: contains the different urls and what they do when receiving a POST or GET request
Run: Simply the code for running the application

## Setup & Installation

Acces to internet, pyhton version >=3.12.3.


## Starting The Web Application

Run the code below:
```bash
python run.py
```

## Viewing The Web Application

Go to 
```
http://127.0.0.1:5000
```
Other pages: 
```
http://127.0.0.1:5000/login
```
```
http://127.0.0.1:5000/signup
```
Only accessible with an account:
```
http://127.0.0.1:5000/shoppinglist
```