# todoapp.py
from flask import Flask, render_template, request, redirect, url_for, flash # Added flash
import re # For email validation

app = Flask(__name__)
# You need a secret key to use flash messages for feedback (optional but good practice)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # Change this to a random secret key

# Global list to store To-Do items.
# Each item is a dictionary.
todo_list = []

@app.route('/')
def index():
    """Renders the main page with the to-do list and forms."""
    return render_template('index.html', items=todo_list) # Pass the list to the template [cite: 10]

@app.route('/submit', methods=['POST']) # Route accepts POST requests [cite: 11]
def submit():
    """Handles the submission of a new to-do item."""
    task = request.form.get('task') # Get data from form [cite: 26]
    email = request.form.get('email') # Get data from form [cite: 26]
    priority = request.form.get('priority') # Get data from form [cite: 26]

    # --- Data Validation --- [cite: 30]
    # Basic check for empty fields
    if not task or not email or not priority:
        flash('Error: All fields are required.') # Optional feedback [cite: 31]
        return redirect(url_for('index')) # Redirect back on error

    # Email validation using regex (adjust regex as needed) [cite: 30]
    # Simple regex example: checks for something@something.something
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        flash('Error: Invalid email format.') # Optional feedback [cite: 31]
        return redirect(url_for('index')) # Redirect back on error

    # Priority validation [cite: 30]
    valid_priorities = ['Low', 'Medium', 'High']
    if priority not in valid_priorities:
        flash('Error: Invalid priority value.') # Optional feedback [cite: 31]
        return redirect(url_for('index')) # Redirect back on error

    # --- Add Item if Validation Passes --- [cite: 32]
    todo_list.append({'task': task, 'email': email, 'priority': priority})
    flash('New item added successfully!') # Optional success feedback

    return redirect(url_for('index')) # Redirect to the main page to show the updated list [cite: 11, 32]

@app.route('/clear', methods=['POST']) # Route accepts POST requests [cite: 12, 36]
def clear():
    """Clears all items from the to-do list."""
    global todo_list # Required if you re-assign the global variable
    todo_list = [] # Clear the list [cite: 34]
    # Or use todo_list.clear()
    flash('List cleared.') # Optional feedback
    return redirect(url_for('index')) # Redirect back to the main page [cite: 35]

if __name__ == '__main__':
    # debug=True allows automatic reloading during development and shows detailed errors
    # Remove debug=True or set to False for production/final submission
    app.run(debug=True, host='0.0.0.0', port=5000) # Makes it accessible on http://localhost:5000 [cite: 13]
