from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image
import numpy as np

app = Flask(__name__)

# Set the folder where images will be stored
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Function to check file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route for the homepage
@app.route('/')
def homepage():
    return render_template('homepage.html')  # This will render the homepage template

# Route for uploading the image
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the file part is in the request
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Save the file to the upload folder
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Open the image and calculate the average color
            img = Image.open(filename)
            img = img.convert('RGB')
            img_array = np.array(img)
            avg_color = img_array.mean(axis=(0, 1))  # Calculate the average color
            r, g, b = int(avg_color[0]), int(avg_color[1]), int(avg_color[2])

            # Redirect to result page with RGB values and filename
            return redirect(url_for('result', r=r, g=g, b=b, filename=file.filename))

    return render_template('upload.html')

# Route for displaying the result
@app.route('/result')
def result():
    r = int(request.args.get('r'))
    g = int(request.args.get('g'))
    b = int(request.args.get('b'))
    filename = request.args.get('filename')

    return render_template('result.html', r=r, g=g, b=b, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
