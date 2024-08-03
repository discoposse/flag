from flask import Flask, request, send_file, render_template_string
import os
import subprocess

app = Flask(__name__)
image_path = "/home/discoposse/Desktop/gtm-delta.png"
image_directory = "/home/discoposse/Desktop/images"
image_files = ["image1.png", "image2.png", "image3.png"]  # List your image filenames here

@app.route('/')
def index():
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
    return render_template_string(html, images=image_files)

@app.route('/change-image', methods=['POST'])
def change_image():
    global image_path
    selected_image = request.form.get('image')
    if selected_image not in image_files:
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
    
    # Add to image list if not already there
    if file.filename not in image_files:
        image_files.append(file.filename)

    return "Image uploaded successfully", 200

@app.route('/current-image', methods=['GET'])
def current_image():
    return send_file(image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

