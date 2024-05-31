from flask import json, jsonify, render_template, request,  Blueprint, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

from models import Staple, Grocery, User
from forms import signupForm, loginForm
from sqlalchemy import exc


def register_routes(app, db, bcrypt):
    """
    Registers the differen routes (web pages) of the application.
    Is automatically called on in create_app(), no need to change the arguments if not changing the name of app, db, and bycrypt in main.
    :param app: app created in main.py
    :param db: database created in main.py
    :param bcrypt: bycrypt encryption created in main.py
    :return: different html pages
    """
    
    @app.route("/", methods=["GET", "POST"])
    def home():
    """
    Returns the template for the home page.
    """
        return render_template("home.html")
    
    @app.route("/shoppinglist", methods=["GET", "POST"])
    @login_required # Page only visible when logged in
    def shoppinglist():
    """
    Returns the template for the shoppinglist page.
    Determines the type of request being made. If just a GET it will render the page, if a POST it will add the information into the database and return the updated page.
    """
        if request.method == "POST":
            # Get information from the form and add new item to the database
            staple = request.form.get("staple")
            grocery = request.form.get("grocery")
            if staple:
                new_staple = Staple(staple=staple, user_id=current_user.id)
                db.session.add(new_staple)
                db.session.commit()
                return render_template("shoppinglist.html", user=current_user)
            elif grocery:
                new_grocery = Grocery(grocery=grocery, user_id=current_user.id)
                db.session.add(new_grocery)
                db.session.commit()
                return render_template("shoppinglist.html", user=current_user)
        elif request.method == "GET":
            return render_template("shoppinglist.html", user=current_user)
    
    
    @app.route('/delete-staple', methods=['POST'])
    def delete_staple():  
    """
    Deletes a staple from the data base and the shoppinglist page. Returns through a javascript function the updated shoppinglist page. 
    """
        staple = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
        stapleId = staple['stapleId']
        staple = Staple.query.get(stapleId)
        if staple:
            if staple.user_id == current_user.id:
                db.session.delete(staple)
                db.session.commit()

        return jsonify({})
    
    @app.route('/delete-grocery', methods=['POST'])
    def delete_grocery():  
    """
    Deletes a grocery from the data base and the grocerylist, if item was a staple it is returned to the staple list and database. 
    Returns through a javascript function the updated shoppinglist page. 
    """
        grocery = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
        groceryId = grocery['groceryId']
        grocery = Grocery.query.get(groceryId)
        if grocery:
            if grocery.user_id == current_user.id:
                if grocery.was_staple:
                    new_staple = Staple(staple=grocery.grocery, user_id=current_user.id)
                    db.session.add(new_staple)
                    db.session.delete(grocery)
                    db.session.commit()
                else:
                    db.session.delete(grocery)
                    db.session.commit()

        return jsonify({})
    
    @app.route('/check-staple', methods=['POST'])
    def check_staple():  
    """
    Deletes a pantry staple from the data base and the shoppinglist when it is checked of on the shopppinglist page.
    It adds the item to the database as a grocery and adds it to the grocery list.
    Returns through a javascript function the updated shoppinglist page. 
    """
        staple = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
        stapleId = staple['stapleId']
        staple = Staple.query.get(stapleId)
        if staple:
            if staple.user_id == current_user.id:
                new_grocery = Grocery(grocery=staple.staple, user_id=current_user.id, was_staple=True)
                db.session.add(new_grocery)
                db.session.delete(staple)
                db.session.commit()

        return jsonify({})
    
        
    @app.route("/signup", methods=["GET", "POST"])
    def signup():
    """
    Signs a user up. 
    Function checks the form input. 
    If invalid returns the signup page with error messages.
    If valid, then creates a hash for the password and saves the information for the user in the database and returns the login page. 
    """
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = signupForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        return render_template("signup.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
    """
    Logs a user in. 
    Function checks the form input. 
    If invalid returns the login page with error messages.
    If valid, then checks for an account with that information and logs the user in and returns the shoppinglist page. 
    """
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = loginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('shoppinglist'))
            else:
                flash('Login Failed, check Username and Password', 'danger')
        return render_template('login.html', title='Login', form=form)
            
    @app.route("/logout")
    @login_required # Page only visible when logged in
    def logout():
    """
    Logs a user out. 
    Function logs out user and returns the home page. 
    """
        logout_user()
        return render_template("home.html")
                
            
        
