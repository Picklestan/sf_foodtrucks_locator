import os
import re
from postgres import get_trucks_locations, add_user, get_user
from flask import Flask, render_template, jsonify, Response, request, session, redirect
from flask import request
from saltgen import generate_salt
import hashlib


app = Flask(__name__, template_folder="./templates")
app.secret_key = 'IzaSyCzw3oN4c9zVUh'


@app.route("/")
def render_index_page():
    return render_template('index.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    msg = ''

    if request.method == "POST":
        username = request.form.get("name")
        password = request.form.get("password")
        session["name"] = username
        account = get_user(username)

        if not account:
            msg = 'Account with this name does not exist'
            return render_template("login.html", msg=msg)

        salt = account[0][3]
        hashed_password = hashlib.sha256(str.encode(salt + password)).hexdigest()
        print(hashed_password)
        print('[ass', account[0][1])
        if hashed_password != account[0][1]:
            msg = 'You have entered the wrong password!'
            return render_template("login.html", msg=msg)

        return redirect("/")
    return render_template("login.html", msg=msg)



@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route('/trucks', methods = ['GET'])
def get_trucks():
    lon = request.args.get('lon')
    lat = request.args.get('lat')
    data = get_trucks_locations(lat, lon)
    return jsonify(data)




@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = get_user(username)
        print(account)

        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            salt = generate_salt()
            hashed_password = hashlib.sha256(str.encode(salt+password)).hexdigest()
            add_user(username, hashed_password, email, salt)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

app.run()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#session(app)


if __name__ == '__main__':
    app.run()



