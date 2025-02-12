from flask import Flask, request, session, redirect, url_for, render_template_string
import hashlib
import time

app = Flask(__name__)

# In-memory database simulation (user login data store)
user_db = {}

# Secret key for session management (in production, it should be more secure)
app.secret_key = 'your_secret_key_here'

# Simulating the in-memory database for user sessions
def get_user_session(user_id):
    return user_db.get(user_id)

def store_user_session(user_id, data):
    user_db[user_id] = data

# Simulating ALB Stickiness with user-session cookies
@app.route('/')
def home():
    if 'user_id' in session:
        return f"Hello, {session['user_id']}! You are logged in."
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check the user credentials (simulating a simple authentication)
        user_id = username  # In real life, this would be a user ID or email
        stored_user = get_user_session(user_id)
        
        if stored_user and stored_user['password'] == password:
            # User successfully authenticated, create a session
            session['user_id'] = user_id
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials, please try again!'
    
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    # Clear the session
    session.pop('user_id', None)
    return redirect(url_for('home'))

# Simulate user registration or storage in the in-memory DB
@app.route('/register/<username>/<password>')
def register(username, password):
    user_id = username
    # Simulate storing the password in a simple form (plain text)
    store_user_session(user_id, {'password': password, 'timestamp': time.time()})
    return f"User {username} registered successfully!"

# Main entry point for the application
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
