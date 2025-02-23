# Import necessary functions and classes from the Flask library.
from flask import Flask, render_template, request, redirect, url_for

# Create an instance of the Flask class. This instance is our WSGI application.
app = Flask(__name__)

# Define a route for the homepage ('/').
@app.route('/')
def home():
    # Render and return the HTML template 'home.html' located in the 'templates' folder.
    return render_template('home.html')

# Define a route for the color selection page ('/colors').
# We allow both GET and POST methods because:
# - GET is used when first arriving at the page.
# - POST is used when the user submits the form (i.e., selects a color).
@app.route('/colors', methods=['GET', 'POST'])
def colors():
    # Check if the form on the page was submitted using a POST request.
    if request.method == 'POST':
        # Retrieve the value of 'color' from the submitted form data.
        color = request.form.get('color')
        # If a color was selected (i.e., the color variable is not empty)
        if color:
            # Redirect the user to the 'result' route.
            # The chosen color is passed as a URL parameter (query string) with the key 'chosen_color'.
            return redirect(url_for('result', chosen_color=color))
    # If the request method is GET (or no valid form data was submitted), display the color selection page.
    return render_template('color.html')

# Define a route for the result page ('/result').
@app.route('/result')
def result():
    # Retrieve the 'chosen_color' parameter from the URL query string.
    # If it doesn't exist, default to the string 'None'.
    chosen_color = request.args.get('chosen_color', 'None')
    # Render the 'result.html' template, passing the chosen color as a variable called 'color'
    # so it can be used in the HTML template.
    return render_template('result.html', color=chosen_color)

# This conditional ensures the Flask app runs only if this script is executed directly.
# 'debug=True' enables debug mode, which is useful during development.
if __name__ == '__main__':
    app.run(debug=True)
