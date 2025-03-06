'''''
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo.server_api import ServerApi
from pymongo import MongoClient
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'

users_db = {
    "testuser": {"password": "password123"}
}

# MongoDB connection
uri = "mongodb+srv://2310030055:bhavishya123456789@cluster0.mry6i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['flask_db']  # The database to use
users_collection = db['users']  # The collection (table) for users

# Route for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        password = request.form['password']

        # In a real app, you'd want to store this in a database
        if users_collection.find_one({"username": username}):
            return "User already exists, try a different username."

            # Insert the new user into the database
        users_collection.insert_one({"username": username, "password": password})
        return redirect(url_for('login.html'))  # Redirect to login after successful registration

    return render_template('login.html')


# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and password matches
        user = users_collection.find_one({"username": username})
        if user and user['password'] == password:
            session['user'] = username  # Store username in session to track the user
            return redirect(url_for('only'))  # Redirect to the next page (only.html)
        else:
            return "Invalid credentials, please try again."

    return redirect(url_for('only'))
@app.route('/')
def home():
    return render_template('focara.html')

# Route for the 'only.html' page after login
@app.route('/only')
def only():
    if 'user' in session:  # Check if the user is logged in
        return render_template('only.html')
    else:
        return redirect(url_for('login.html'))  # If not logged in, redirect to login page


if __name__ == '__main__':
    app.run(debug=True)
'''
'''''
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo.server_api import ServerApi
from pymongo import MongoClient
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'

users_db = {
    "testuser": {"password": "password123"}
}

# MongoDB connection
uri = "mongodb+srv://2310030055:bhavishya123456789@cluster0.mry6i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['flask_db']  # The database to use
users_collection = db['users']  # The collection (table) for users

# Route for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        password = request.form['password']

        # In a real app, you'd want to store this in a database
        if users_collection.find_one({"username": username}):
            return "User already exists, try a different username."

            # Insert the new user into the database
        users_collection.insert_one({"username": username, "password": password})
        return redirect(url_for('login.html'))  # Redirect to login after successful registration

    return render_template('login.html')


# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and password matches
        user = users_collection.find_one({"username": username})
        if user and user['password'] == password:
            session['user'] = username  # Store username in session to track the user
            return redirect(url_for('only'))  # Redirect to the next page (only.html)
        else:
            return "Invalid credentials, please try again."

    return redirect(url_for('only'))
@app.route('/')
def home():
    return render_template('focara.html')

# Route for the 'only.html' page after login
@app.route('/only')
def only():
    if 'user' in session:  # Check if the user is logged in
        return render_template('only.html')
    else:
        return redirect(url_for('login.html'))  # If not logged in, redirect to login page


if __name__ == '__main__':
    app.run(debug=True)
'''

from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # To enable session and flash messages

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Update with your connection string if needed
db = client['flask_db']
users_collection = db['users']

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = users_collection.find_one({'username': username})  # Check user in MongoDB

        if user and user['password'] == password:
            session['username'] = username  # Store username in session
            return redirect(url_for('only'))  # Redirect to only.html
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username') # Trim spaces and convert to lowercase
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password cannot be empty.', 'danger')
            return redirect(url_for('register'))

        existing_user = users_collection.find_one({'username': username})  # Check if username exists

        if existing_user:
            flash('Username already taken. Please choose another one.', 'danger')
        else:
            users_collection.insert_one({'username': username, 'password': password})
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('focara.html')

@app.route('/only')
def only():
    if 'username' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))

    return render_template('only.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
