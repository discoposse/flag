# DiscoPosse Mic Flag

### What it does

This is a simple flask app that runs on a RaspberryPi 3B+ for a digital microphone flag.

```python
from flask import Flask, request, send_file, render_template_string
import os
import subprocess

app = Flask(__name__)
image_path = "/home/discoposse/Public/flag/gtm-delta.png"
image_directory = "/home/discoposse/Public/flag/images"
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

@app.route('/current-image', methods=['GET'])
def current_image():
    return send_file(image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Explanation:
1. **Index Route (`/`)**:
    - Serves the HTML page with a dropdown to select an image and a submit button.

2. **Change Image Route (`/change-image`)**:
    - Handles the form submission.
    - Validates the selected image.
    - Copies the selected image to the destination path.
    - Kills the existing Chromium browser instance.
    - Starts a new Chromium browser instance in kiosk mode displaying the new image.

3. **Current Image Route (`/current-image`)**:
    - Allows viewing the currently displayed image.

### Step-by-Step:
1. **Create the Flask Application**:
    - Save the updated `image_changer.py`.

2. **Start the Flask Application**:
    ```bash
    python image_changer.py
    ```

3. **Access the Web Interface**:
    - Open a web browser and navigate to `http://<raspberry_pi_ip>:5000/`.

4. **Change the Image**:
    - Use the dropdown to select a new image and submit the form.
    - The Chromium browser on the Raspberry Pi will restart and display the new image.

### Auto-Start Flask Application:
To ensure the Flask application starts automatically on boot, add it to your crontab:

```bash
crontab -e
```

Add the following line:

```bash
@reboot /usr/bin/python3 /path/to/image_changer.py &
```

Replace `/path/to/image_changer.py` with the full path to your script.

### Summary:
This setup allows you to change the displayed image on the Raspberry Pi through a web interface, automatically refreshing the Chromium browser to reflect the changes without needing a reboot.

```bash
curl -F 'file=@/home/discoposse/Public/flag/images/snia-eod.png' http://discopi.local:5000/upload-image
```

My config

image_path = "/home/discoposse/Public/flag/images/gtm-delta.png"
image_directory = "/home/discoposse/Public/flag/images"
image_files = ["gtm-delta.png", "discoposse-podcast.png", "snia-eod.png"]  

