from flask import Flask, render_template, request, jsonify, redirect, url_for,flash,session
import csv
import random
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import matplotlib.pyplot as plt
import io
import base64
from flask import send_file
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='hi'


db = SQLAlchemy(app)
#models made
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Function to calculate BMR
def calculate_bmr(age, height_cm, weight, gender):
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) + 5
    else:  # Female
        bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) - 161
    return bmr

# Function to calculate calorie intake based on BMR and physical activity level
def calculate_calories(bmr, activity_level):
    if activity_level == "Sedentary":
        calorie_intake = bmr * 1.2
    elif activity_level == "Lightly active":
        calorie_intake = bmr * 1.375
    elif activity_level == "Moderately active":
        calorie_intake = bmr * 1.55
    elif activity_level == "Very active":
        calorie_intake = bmr * 1.725
    else:  # Extra active
        calorie_intake = bmr * 1.9
    return calorie_intake

# Function to read meal options from CSV
def read_meal_options(file_path):
    meal_options = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            meal_type, meal, calories = row[0], row[1], float(row[2])
            meal_options.append((meal_type, meal, calories))
    return meal_options

# Function to select one meal randomly from each meal type and find the combination closest to the target calorie count
def select_meals(meal_options, target_calories):
    selected_meals = []
    
    # Create meal dictionaries for each meal type
    meal_dict = {meal_type: [] for meal_type in ["Breakfast", "Lunch", "Snacks", "Dinner"]}
    for meal in meal_options:
        meal_type, meal_name, calories = meal
        meal_dict[meal_type].append((meal_name, calories))
    
    # Randomly select one meal from each meal type
    for meal_type, meals in meal_dict.items():
        selected_meal = random.choice(meals)
        selected_meals.append((meal_type, *selected_meal))
    
    # Find the combination closest to the target calorie count
    closest_combination = selected_meals
    min_difference = abs(sum(meal[2] for meal in selected_meals) - target_calories)
    for _ in range(1000):  # Try 1000 random combinations
        random_combination = [(meal_type, *random.choice(meals)) for meal_type, meals in meal_dict.items()]
        total_calories = sum(meal[2] for meal in random_combination)
        if abs(total_calories - target_calories) < min_difference:
            closest_combination = random_combination
            min_difference = abs(total_calories - target_calories)
    
    return closest_combination

# Function to classify BMI
def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Healthy Weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# Function to display recommended calorie intake and diet plan
@app.route('/previou_ver', methods=['GET', 'POST'])
def display_result():
    if request.method == 'POST':
        try:
            # Get form data
            age = int(request.form['age'])
            height_cm = float(request.form['height'])
            weight = float(request.form['weight'])
            gender = request.form['gender']
            activity_level = request.form['activity']
            diet_type = request.form['diet']

            # Calculate BMR and calorie intake
            bmr = calculate_bmr(age, height_cm, weight, gender)
            calorie_intake = calculate_calories(bmr, activity_level)

            # Read meal options based on diet type
            if diet_type == "Vegan":
                meal_options = read_meal_options("vegan.csv")
            elif diet_type == "Vegetarian":
                meal_options = read_meal_options("veg.csv")
            else:
                meal_options = read_meal_options("non-veg.csv")

            # Select meals
            selected_meals = select_meals(meal_options, calorie_intake)

            # Classify BMI
            bmi = (weight / ((height_cm / 100) ** 2))
            bmi_classification = classify_bmi(bmi)

            # Prepare data for rendering
            result_data = {
                'bmi': f"{bmi:.2f} ({bmi_classification})",
                'calorie_intake': f"{calorie_intake:.2f}",
                'diet_plan': selected_meals
            }

            return render_template('result.html', result=result_data)

        except ValueError:
            error_message = "Please enter valid age, height, and weight."
            return render_template('error.html', error=error_message)

    return render_template('index.html')

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('fitness.db')
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to authenticate user
def authenticate_user(conn, username, password):
    sql_select_user = """
        SELECT * FROM User WHERE username = ? AND password = ?;
    """
    cursor = conn.cursor()
    cursor.execute(sql_select_user, (username, password))
    row = cursor.fetchone()
    if row:
        return True
    return False

def create_user(conn, username, password):
    try:
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            # Username already exists
            return False

        # Insert the new user into the database
        cursor.execute("INSERT INTO User (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except Exception as e:
        print("Error creating user:", e)
        return False

@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Create a connection to the database
        conn = create_connection()
        session['username'] = username  # Set the username in the session
        # Authenticate user
        if authenticate_user(conn, username, password):
            print('sesion user set')
            session['username'] = username  # Set the username in the session
            return redirect(url_for('index2'))  # Redirect to index2 route
        else:
           flash("Invalid username or password. Please try again.",'error')
           return redirect(url_for('login_page'))
    else:
        # Render the login page for GET requests
        return render_template('login.html')
        
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if password and confirm password match
        if password != confirm_password:
            flash("Passwords do not match. Please try again.", 'error')
            return redirect(url_for('signup'))  # Redirect back to signup page with flash message
            
        # Create a connection to the database
        conn = create_connection()

        # Create the new user in the database
        if create_user(conn, username, password):
            flash("User created successfully!", 'success')
            return redirect(url_for('login_page'))  # Redirect to login page after successful signup
        else:
            flash("Failed to create user. Please try again.", 'error')
            return redirect(url_for('signup'))  # Redirect back to signup page with flash message
    else:
        # Render the signup page for GET requests
        return render_template('signup.html')

    
@app.route('/index2', methods=['GET', 'POST'])
def index2():
    if 'username' in session:
        username = session['username']  # Get the username from the session
        user_id = get_user_id(username)
        conn = create_connection()
        cursor = conn.cursor()
                    
        cursor.execute('SELECT SUM(calories_consumed), SUM(calories_burned) FROM Progress WHERE user_id = ?', (user_id,))
        totals = cursor.fetchone()
        total_calories_consumed, total_calories_burned = totals if totals else (0, 0)


        if request.method == 'POST':
            try:
                # Get form data
                age = int(request.form['age'])
                height_cm = float(request.form['height'])
                weight = float(request.form['weight'])
                gender = request.form['gender']
                activity_level = request.form['activity']
                diet_type = request.form['diet']

                # Calculate BMR and calorie intake
                bmr = calculate_bmr(age, height_cm, weight, gender)
                calorie_intake = calculate_calories(bmr, activity_level)

                # Read meal options based on diet type
                if diet_type == "Vegan":
                    meal_options = read_meal_options("vegan.csv")
                elif diet_type == "Vegetarian":
                    meal_options = read_meal_options("veg.csv")
                else:
                    meal_options = read_meal_options("non-veg.csv")

                # Select meals
                selected_meals = select_meals(meal_options, calorie_intake)

                # Classify BMI
                bmi = (weight / ((height_cm / 100) ** 2))
                bmi_classification = classify_bmi(bmi)

                # Prepare data for rendering
                result_data = {
                    'bmi': f"{bmi:.2f} ({bmi_classification})",
                    'calorie_intake': f"{calorie_intake:.2f}",
                    'diet_plan': selected_meals
                }
            
                conn = create_connection()
                cursor = conn.cursor()
                    
                cursor.execute('SELECT SUM(calories_consumed), SUM(calories_burned) FROM Progress WHERE user_id = ?', (user_id,))
                totals = cursor.fetchone()
                total_calories_consumed, total_calories_burned = totals if totals else (0, 0)


                return render_template('index2.html', username=username, result_data=result_data,total_calories_burned=total_calories_burned,total_calories_consumed=total_calories_consumed)

            except ValueError:
                error_message = "Please enter valid age, height, and weight."
                return render_template('error.html', error=error_message)

        else:
            # Define an empty result_data dictionary for GET requests
            result_data = {}

        # Render the index2 template for GET requests
        return render_template('index2.html', username=username, result_data=result_data,total_calories_burned=total_calories_burned,total_calories_consumed=total_calories_consumed)
    else:
        # Handle the case when the user is not logged in
        return redirect(url_for('login_page'))
    
# @app.route('/track_progress',methods=['GET','POST'])
# def track_progress():
#     if 'username' in session:
#         username = session['username']  # Get the username from the session
#     return render_template('track_progress.html',username=username)

# def track_progress():
#     if 'username' in session:
#         username = session['username']  # Get the username from the session
#         if request.method == 'POST':
#             user_id = get_user_id(username)  # Function to get user ID from username
#             date = request.form['date']
#             weight = float(request.form['weight'])
#             height = float(request.form['height'])
#             bmi = weight / ((height / 100) ** 2)
#             calories_consumed = int(request.form['calories_consumed'])
#             calories_burned = int(request.form['calories_burned'])

#             # Insert data into Progress table
#             conn = create_connection()
#             cursor = conn.cursor()
#             cursor.execute('''INSERT INTO Progress (user_id, date, weight, height, bmi, calories_consumed, calories_burned)
#                               VALUES (?, ?, ?, ?, ?, ?, ?)''', (user_id, date, weight, height, bmi, calories_consumed, calories_burned))
#             conn.commit()
#             conn.close()

#             return redirect(url_for('generate_report'))
#         return render_template('track_progress.html', username=username)
#     else:
#         return redirect(url_for('login_page'))

# Function to get user ID from username
def get_user_id(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM User WHERE username = ?', (username,))
    user_id = cursor.fetchone()[0]
    conn.close()
    return user_id

# Track progress route
@app.route('/track_progress', methods=['GET', 'POST'])
def track_progress():
    if 'username' in session:
        username = session['username']  # Get the username from the session
        user_id = get_user_id(username)  # Function to get user ID from username

        if request.method == 'POST':
            try:
                date = request.form['date']
                weight = float(request.form['weight'])
                height = float(request.form['height'])
                bmi = weight / ((height / 100) ** 2)
                calories_consumed = int(request.form['calories_consumed'])
                calories_burned = int(request.form['calories_burned'])

                # Insert data into Progress table
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO Progress (user_id, date, weight, height, bmi, calories_consumed, calories_burned)
                                  VALUES (?, ?, ?, ?, ?, ?, ?)''', (user_id, date, weight, height, bmi, calories_consumed, calories_burned))
                conn.commit()
                conn.close()
            except ValueError:
                return render_template('track_progress.html', username=username, error="Please enter valid data.")

        # Fetch progress data for the user
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT date, weight, bmi FROM Progress WHERE user_id = ? ORDER BY date', (user_id,))
        data = cursor.fetchall()
        conn.close()

        dates = [datetime.datetime.strptime(row[0], '%Y-%m-%d').date() for row in data]
        weights = [row[1] for row in data]
        bmis = [row[2] for row in data]

        # Generate graph
        plt.figure(figsize=(10, 5))
        plt.plot(dates, weights, label='Weight (kg)', marker='o')
        plt.plot(dates, bmis, label='BMI', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Values')
        plt.title('Progress Over Time')
        plt.legend()
        plt.grid(True)

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template('track_progress.html', username=username, plot_url=plot_url)

    else:
        return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(debug=True)