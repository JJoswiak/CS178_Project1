# CS178 Flask Movie App

# This is a web application that allows users to sign up, log in, and manage a movie database. The app demonstrates integration with both AWS DynamoDB and AWS RDS (MySQL) to handle user authentication and CRUD operations on movie data.

---

## Project Summary

# - Users can sign up and log in using secure password hashing (stored in DynamoDB).
# - Once authenticated, users can:
# - Create new movie entries
# - Read all saved movies
# - Delete movies
# - Access to movie-related pages is restricted to logged-in users using Flask session management.

---

## Technologies Used

# - Flask – Web framework
# - HTML + Jinja2 – Templating engine for frontend
# - AWS DynamoDB – NoSQL database for user accounts
# - AWS RDS (MySQL) – SQL database for storing movie data
# - Werkzeug Security – Secure password hashing and checking
# - Python 3

---

## Setup & Run Instructions

# - Clone the Repository
# - Install Required Packages
# - Update Your AWS Credentials
# - Run the App
