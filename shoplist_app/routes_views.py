from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from models import Staple, ShoppingItem, User

def register_routes(app, db):
    @app.route("/")
    def home():
        return render_template("home.html")
    
    @app.route("/sign-up", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            password2 = request.form["password2"]

            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already linked to an account', category='error') 
            elif len(email) < 4:
                flash('Email is not valid', category='error')
            elif len(username) < 2:
                flash('First name is too short', category='error')
            elif password != password2:
                flash('Please make sure passwords match', category='error')
            elif len(password) < 7:
                flash('Password should contain at least 7 characters', category='error')
            else:
                new_user = User(username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(user, remember=True)
                flash('Account created', category='success')
                return redirect(url_for('home'))
            
        return render_template("sign_up.html", user=current_user)
    
    
    @app.route("/add", methods=["POST"])
    def add():
        staple = request.form["staple"]
        new_staple = Staple(staple=staple)
        db.session.add(new_staple)
        db.session.commit()
        return redirect(url_for("home"))
    
    @app.route("/delete/<int:id>")
    def delete(id):
        staple = Staple.query.get(id)
        db.session.delete(staple)
        db.session.commit()
        return redirect(url_for("home"))
    

    @app.route("/login", methods=["GET", "POST"])
    def login():
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        return render_template("logout.html")