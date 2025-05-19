# app.py

from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import pandas as pd
from flask import jsonify 
import pyttsx3
from flask import send_file

# Initialize the Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load color dataset
csv_path = 'colors.csv' 
color_data = pd.read_csv(csv_path)

# Function to get closest color name
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = "Unknown"
    for i in range(len(color_data)):
        r_d = abs(R - int(color_data.loc[i, "R"]))
        g_d = abs(G - int(color_data.loc[i, "G"]))
        b_d = abs(B - int(color_data.loc[i, "B"]))
        distance = r_d + g_d + b_d
        if distance < minimum:
            minimum = distance
            cname = color_data.loc[i, "color_name"]
    return cname

# Route for home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle uploaded image
        image_file = request.files['image']
        if image_file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
            image_file.save(filepath)
            return redirect(url_for('detect', filename=image_file.filename))
    return render_template('index.html')

# Route to display image and handle color detection
@app.route('/detect/<filename>')
def detect(filename):
    return render_template('detect.html', filename=filename)

@app.route('/get_color')
def get_color():
    filename = request.args.get('filename')
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))

    # Load image again
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = cv2.imread(image_path)

    if x >= img.shape[1] or y >= img.shape[0]:
        return jsonify({'error': 'Invalid coordinates'})

    b, g, r = img[y, x]  # Get BGR at (x, y)
    r, g, b = int(r), int(g), int(b)
    color_name = get_color_name(r, g, b)

    return jsonify({'color': color_name, 'r': r, 'g': g, 'b': b})


# Add this route at the bottom of app.py
@app.route('/speak_color')
def speak_color():
    color = request.args.get('color')
    r = request.args.get('r')
    g = request.args.get('g')
    b = request.args.get('b')

    # Prepare text to speak
    text = f"This color is {color}"

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
    return '', 204  # No content (just perform the speech)

@app.route('/about')
def about():
    return render_template('about.html')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
