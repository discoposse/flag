from flask import Flask, request, send_file, render_template_string
import os
import subprocess

app = Flask(__name__)
image_path = "/home/discoposse/Public/flag/image/gtm-delta.png"
image_directory = "/home/discoposse/Public/flag/images"

def get_image_files():
    return [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))]

@app.route('/')
def index():
    images = get_image_files()
    html = '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Change Image</title>
      </head>
      <body>
        <h1>Change Image</h1>
        <form action="/change-image" method="post">
          <label for="image">Choose an image:</label>
          <select name="image" id="image">
            {% for image in images %}
              <option value="{{ image }}">{{ image }}</option>
            {% endfor %}
          </select>
          <input type="submit" value="Submit">
        </form>
        <h1>Upload New Image</h1>
        <form action="/upload-image" method="post" enctype="multipart/form-data">
          <input type="file" name="file" id="file">
          <input type="submit" value="Upload">
        </form>
      </body>
    </html>
    '''
    return render_template_string(html, images=images)

@app.route('/change-image', methods=['POST'])
def change_image():
    global image_path
    selected_image = request.form.get('image')
    if not selected_image or not os.path.isfile(os.path.join(image_directory, selected_image)):
        return "Invalid image selected", 400

    new_image_path = os.path.join(image_directory, selected_image)
    os.system(f'cp {new_image_path} {image_path}')

    # Reload the Chromium browser
    subprocess.run(["pkill", "chromium"])
    subprocess.Popen(["chromium-browser", "-kiosk", image_path])

    return "Image updated successfully", 200

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    file_path = os.path.join(image_directory, file.filename)
    file.save(file_path)
    
    return "Image uploaded successfully", 200

@app.ro
