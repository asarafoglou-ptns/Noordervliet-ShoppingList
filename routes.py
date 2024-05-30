from flask import json, jsonify, render_template, request,  Blueprint, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

from models import Staple, Grocery, User
from forms import signupForm, loginForm
from sqlalchemy import exc


def register_routes(app, db, bcrypt):
    
    @app.route("/", methods=["GET", "POST"])
    def home():
        return render_template("home.html")
    
    @app.route("/shoppinglist", methods=["GET", "POST"])
    def shoppinglist():
        if request.method == "POST":
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
    @login_required
    def logout():
        logout_user()
        return render_template("home.html")
                
            
        