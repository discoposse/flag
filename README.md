Here's a `README.md` file for your project:

```markdown
# Raspberry Pi Digital Signage with Flask and Chromium

This project allows you to use a Raspberry Pi to display an image in a headless Chromium browser in kiosk mode. The displayed image can be changed via a simple web interface or an API call without rebooting the device.

## Features
- Dynamically list and select images from a specified directory.
- Upload new images via a web interface.
- Automatically refresh the Chromium browser to display the new image.

## Prerequisites
- Raspberry Pi with Raspbian OS
- Python 3.x
- Flask (`pip install flask`)
- Chromium browser

## Installation

1. **Clone the repository** (if applicable) or create the script file:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install Flask**:

    ```bash
    pip install flask
    ```

3. **Create the required directories and files**:

    ```bash
    mkdir -p /home/discoposse/Desktop/images
    touch /home/discoposse/Desktop/gtm-delta.png
    ```

4. **Place your image files in the images directory**:

    ```bash
    mv /path/to/your/images/*.png /home/discoposse/Desktop/images/
    ```

5. **Save the script** as `image_changer.py`:

    ```python
    from flask import Flask, request, send_file, render_template_string
    import os
    import subprocess

    app = Flask(__name__)
    image_path = "/home/discoposse/Desktop/gtm-delta.png"
    image_directory = "/home/discoposse/Desktop/images"

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

    @app.route('/current-image', methods=['GET'])
    def current_image():
        return send_file(image_path, mimetype='image/png')

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
    ```

## Usage

1. **Start the Flask application**:

    ```bash
    python image_changer.py
    ```

2. **Access the web interface**:

    Open a web browser and navigate to `http://<raspberry_pi_ip>:5000/`. Replace `<raspberry_pi_ip>` with the IP address of your Raspberry Pi.

3. **Change the displayed image**:

    - **Select an image** from the dropdown list and click "Submit" to change the displayed image.
    - **Upload a new image** using the upload form. After uploading, the new image will be available in the dropdown list.

4. **View the current image**:

    Navigate to `http://<raspberry_pi_ip>:5000/current-image` to see the currently displayed image.

## Auto-Start the Flask Application

To ensure the Flask application starts automatically on boot, add it to your crontab:

1. **Edit the crontab**:

    ```bash
    crontab -e
    ```

2. **Add the following line**:

    ```bash
    @reboot /usr/bin/python3 /path/to/image_changer.py &
    ```

    Replace `/path/to/image_changer.py` with the full path to your script.

## License

This project is licensed under the MIT License.
```

This `README.md` file provides an overview of the project, installation instructions, usage guidelines, and steps to set up the Flask application to start automatically on boot. Adjust paths and filenames as necessary to match your specific setup.

```bash

```

## My config

image_path = "/home/discoposse/Public/flag/images/gtm-delta.png"
image_directory = "/home/discoposse/Public/flag/images"
image_files = ["gtm-delta.png", "discoposse-podcast.png", "snia-eod.png"]  

curl -F 'file=@/home/discoposse/Public/flag/images/discoposse-podcast.png' http://discopi.local:5000/change-image