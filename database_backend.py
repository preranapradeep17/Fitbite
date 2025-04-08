import sqlite3

# Connect to the SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect('fitness.db')
cursor = conn.cursor()

# Create User table
cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL
                )''')

# Create Progress table
cursor.execute('''CREATE TABLE IF NOT EXISTS Progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date DATE NOT NULL,
                    weight FLOAT NOT NULL,
                    height FLOAT NOT NULL,
                    bmi FLOAT NOT NULL,
                    calories_consumed INTEGER NOT NULL,
                    calories_burned INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES User(id)
                )''')

# Create Meal table
cursor.execute('''CREATE TABLE IF NOT EXISTS Meal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    meal_type VARCHAR(50) NOT NULL,
                    meal VARCHAR(100) NOT NULL,
                    calories INTEGER NOT NULL,
                    date DATE NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES User(id)
                )''')

# Create VegRecipe table
cursor.execute('''CREATE TABLE IF NOT EXISTS VegRecipe (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    meal_type VARCHAR(50) NOT NULL,
                    meal VARCHAR(100) NOT NULL,
                    calories INTEGER NOT NULL
                )''')

# Create VeganRecipe table
cursor.execute('''CREATE TABLE IF NOT EXISTS VeganRecipe (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    meal_type VARCHAR(50) NOT NULL,
                    meal VARCHAR(100) NOT NULL,
                    calories INTEGER NOT NULL
                )''')

# Create NonVegRecipe table
cursor.execute('''CREATE TABLE IF NOT EXISTS NonVegRecipe (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    meal_type VARCHAR(50) NOT NULL,
                    meal VARCHAR(100) NOT NULL,
                    calories INTEGER NOT NULL
                )''')

# Commit changes and close connection
conn.commit()
conn.close()
