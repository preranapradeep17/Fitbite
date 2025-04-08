import csv
import tkinter as tk
from tkinter import ttk, messagebox
import random

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
def display_result():
    try:
        age = int(age_entry.get())
        height_cm = float(height_entry.get())
        weight = float(weight_entry.get())
        gender = gender_var.get()
        activity_level = activity_var.get()

        bmr = calculate_bmr(age, height_cm, weight, gender)
        calorie_intake = calculate_calories(bmr, activity_level)

        if diet_var.get() == "Vegan":
            meal_options = read_meal_options("vegan.csv")
        elif diet_var.get() == "Vegetarian":
            meal_options = read_meal_options("veg.csv")
        else:
            meal_options = read_meal_options("non-veg.csv")

        selected_meals = select_meals(meal_options, calorie_intake)

        diet_plan = ""
        total_calories = 0
        for meal in selected_meals:
            meal_type, meal_name, calories = meal
            diet_plan += f"{meal_type}: {meal_name} - {calories} kcal\n"
            total_calories += calories
        
        # Check if an extra snack can fit
        if total_calories < calorie_intake:
            extra_snack = random.choice([meal for meal in meal_options if meal[0] == "Snacks" and meal[2] <= calorie_intake - total_calories])
            diet_plan += f"Extra Snack: {extra_snack[1]} - {extra_snack[2]} kcal\n"
            total_calories += extra_snack[2]

        bmi = (weight / ((height_cm / 100) ** 2))
        bmi_classification = classify_bmi(bmi)

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Calculated BMI: {bmi:.2f} ({bmi_classification})\n"
                                   f"Recommended calorie intake: {calorie_intake:.2f} kcal/day\n\n"
                                   f"Diet Plan:\n{diet_plan}\n"
                                   f"Total Calories: {total_calories:.2f} kcal")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid age, height, and weight.")

# Tkinter setup
root = tk.Tk()
root.title("FitBite - Calorie Intake and Diet Plan Generator")
root.geometry("600x500")

# Apply theme
style = ttk.Style()
style.theme_use("clam")

# Create custom style for labels
style.configure("CustomLabel.TLabel", background="#f0f0f0", font=("Helvetica", 12), padx=5, pady=5)

# Create custom style for buttons
style.configure("Custom.TButton", font=("Helvetica", 12), padx=10, pady=5)

# Widgets
age_label = ttk.Label(root, text="Age:", style="CustomLabel.TLabel")
age_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
age_entry = ttk.Entry(root)
age_entry.grid(row=0, column=1, padx=10, pady=5)

height_label = ttk.Label(root, text="Height (cm):", style="CustomLabel.TLabel")
height_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
height_entry = ttk.Entry(root)
height_entry.grid(row=1, column=1, padx=10, pady=5)

weight_label = ttk.Label(root, text="Weight (kg):", style="CustomLabel.TLabel")
weight_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
weight_entry = ttk.Entry(root)
weight_entry.grid(row=2, column=1, padx=10, pady=5)

gender_label = ttk.Label(root, text="Gender:", style="CustomLabel.TLabel")
gender_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
gender_var = tk.StringVar()
gender_var.set("Male")
gender_dropdown = ttk.OptionMenu(root, gender_var, "Male", "Female")
gender_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

activity_label = ttk.Label(root, text="Physical Activity:", style="CustomLabel.TLabel")
activity_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
activity_var = tk.StringVar()
activity_var.set("Sedentary")
activity_dropdown = ttk.OptionMenu(root, activity_var, "Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active")
activity_dropdown.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

diet_label = ttk.Label(root, text="Diet Type:", style="CustomLabel.TLabel")
diet_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
diet_var = tk.StringVar()
diet_var.set("Vegan")
diet_dropdown = ttk.OptionMenu(root, diet_var, "Vegan", "Vegetarian", "Non-vegetarian")
diet_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

calculate_button = ttk.Button(root, text="Calculate", command=display_result, style="Custom.TButton")
calculate_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

result_text = tk.Text(root, wrap="word", width=60, height=12, font=("Helvetica", 11))
result_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Expand grid to fill the screen
root.grid_rowconfigure(7, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
