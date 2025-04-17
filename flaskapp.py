from flask import Flask, render_template, request, redirect, url_for, flash, session
import sql_connect
from dynamo_code import create_user, verify_user, hash_password  # Ensure hash_password is available


app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def home():
   # Pass the username from session to the template for personalized greetings
   return render_template('home.html', logged_in='username' in session, username=session.get('username'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
   if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
      
       # Create a user with the provided credentials
       if create_user(username, password):
           flash('Account created. Please log in.', 'success')
           return redirect(url_for('login'))
       else:
           flash('Username already exists or error occurred.', 'danger')
   return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
      
       # Verify the user's credentials
       if verify_user(username, password):
           session['username'] = username  # Store username in the session
           flash('Login successful!', 'success')
           return redirect(url_for('home'))
       else:
           flash('Invalid credentials.', 'danger')
   return render_template('login.html')


@app.route('/logout')
def logout():
   session.pop('username', None)  # Remove the username from session to log out
   flash('Logged out.', 'info')
   return redirect(url_for('login'))


# Ensure that only logged-in users can access these routes
def login_required(route_func):
   def wrapper(*args, **kwargs):
       if 'username' not in session:
           flash("You must be logged in to view this page.", "warning")
           return redirect(url_for('login'))
       return route_func(*args, **kwargs)
   wrapper.__name__ = route_func.__name__
   return wrapper


@app.route('/add-movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if request.method == 'POST':
        title = request.form['title'].strip()

        conn = sql_connect.get_conn()
        cursor = conn.cursor()

        # Check if movie already exists
        cursor.execute('SELECT * FROM movie WHERE title = %s', (title,))
        existing_movie = cursor.fetchone()

        if existing_movie:
            flash('Movie already exists in the database!', 'warning')
        else:
            cursor.execute('INSERT INTO movie (title) VALUES (%s)', (title,))
            conn.commit()
            flash('Movie added successfully!', 'success')

        cursor.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('add_movie.html')


@app.route('/delete-movie', methods=['GET', 'POST'])
@login_required
def delete_movie():
   if request.method == 'POST':
       title = request.form['title']
      
       # Delete the movie from the database
       conn = sql_connect.get_conn()
       cursor = conn.cursor()
       cursor.execute('DELETE FROM movie WHERE title = %s', (title,))
       conn.commit()
       cursor.close()
       conn.close()
      
       flash('Movie deleted successfully!', 'success')
       return redirect(url_for('home'))
  
   return render_template('delete_movie.html')


@app.route('/display-movies')
@login_required
def display_movies():
   # Query to retrieve all movies from the database (removed genre)
   conn = sql_connect.get_conn()
   cursor = conn.cursor()
   cursor.execute('SELECT title FROM movie ORDER BY movie_id DESC')
   movies = cursor.fetchall()
   cursor.close()
   conn.close()
  
   return render_template('display_movies.html', movies=movies)


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080, debug=True)