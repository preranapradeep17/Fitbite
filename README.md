## Table of Contents

- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

FitBite is a fitness application built with Flask that helps users monitor their BMI and suggests appropriate diet plans based on their preferences. The application tracks the user's progress over time and includes a login and signup system for user management. The frontend is built using Bootstrap, HTML, and CSS, and the application also includes a Tkinter implementation for a desktop interface.

## Directory Structure


- **static**: Contains static assets like CSS, JavaScript, images, and vendor libraries.
- **templates**: Contains HTML templates for the Flask application.
- **data**: Contains CSV files with recipe data for different diet types.
- **fitebite.py**: Tkinter implementation for a desktop interface.
- **app.py**: Main Flask application file.
- **requirements.txt**: Lists the dependencies required for the project.

## Technologies Used

- **Python Modules**:
  - **Flask**: Web framework for building the application.
  - **Matplotlib**: Library for creating static, animated, and interactive visualizations in Python.
  - **SQLite**: Database engine for storing user data.
  - **Tkinter**: Standard GUI toolkit for Python.
- **Frontend**:
  - **Bootstrap**: CSS framework for building responsive, mobile-first sites.
  - **HTML**: Markup language for creating web pages.
  - **CSS**: Style sheet language for designing web pages.

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/pranav4004/FITBITE-PYTHON-PROJECT
cd fitbite
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up the database:**

Initialize the SQLite database by running the following commands in the Python shell:

```python
from app import db
db.create_all()
```

5. **Place the CSV files in the data directory:**

Ensure the CSV files (`vegetarian_recipes.csv`, `vegan_recipes.csv`, and `non_vegetarian_recipes.csv`) are in the `data` directory.

## Usage

1. **Run the Flask development server:**

```bash
python app.py
```

2. **Open your browser and navigate to:**

```plaintext
http://localhost:5000
```

Here, you can sign up, log in, calculate your BMI, get diet suggestions, and track your progress.

## Features

- **User Authentication**: Secure login and signup system.
- **BMI Calculation**: Calculate and display the user's Body Mass Index.
- **Diet Suggestions**: Provide diet plans based on user preferences (vegetarian, vegan, non-vegetarian) using data from CSV files.
- **Progress Tracking**: Track and visualize user's progress over time.
- **Desktop Interface**: Tkinter-based desktop application for local use.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin my-feature-branch`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
