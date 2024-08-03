from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)
image_path = "/home/discoposse/Desktop/gtm-delta.png"

@app.route('/change-image', methods=['POST'])
def change_image():
    global image_path
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    file.save(image_path)
    
    # Reload the Chromium browser
    subprocess.run(["pkill", "chromium"])
    subprocess.Popen(["chromium-browser", "-kiosk", image_path])

    return "Image updated successfully", 200

@app.route('/current-image', methods=['GET'])
def current_image():
    return send_file(image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

