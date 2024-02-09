from flask import Flask, request, send_from_directory, render_template, redirect, url_for, send_file
import threading
import os
import requests
from bs4 import BeautifulSoup
import re
import zipfile
from io import BytesIO
import time
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)

IMAGES_DIR = "ebay_images"
IMAGE_LIFETIME = 3600  # Lifetime of images in seconds (e.g., 1 hour)

if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

def purge_old_images():
    """Deletes images that have exceeded their lifetime."""
    for filename in os.listdir(IMAGES_DIR):
        file_path = os.path.join(IMAGES_DIR, filename)
        if os.path.isfile(file_path):
            file_age = time.time() - os.path.getmtime(file_path)
            if file_age > IMAGE_LIFETIME:
                os.remove(file_path)
                print(f"Deleted {filename} due to expiration.")

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(purge_old_images, 'interval', minutes=30)  # Adjust the interval as needed
scheduler.start()

# Remember to shut down the scheduler when closing your app
atexit.register(lambda: scheduler.shutdown())

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ebay_url = request.form.get('ebayUrl')
        if ebay_url:
            # Download images and get filenames
            filenames = download_ebay_listing_images(ebay_url)
            # Redirect to the download page with filenames as query parameters
            return redirect(url_for('download_page', filenames=",".join(filenames)))
    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download_page():
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
    filenames = request.args.get('filenames', '').split(',')
    files = [f for f in filenames if f]  # Filter out empty strings
    return render_template('download.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(IMAGES_DIR, filename, as_attachment=True)

@app.route('/download/all')
def download_all():
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for root, dirs, files in os.walk(IMAGES_DIR):
            for file in files:
                zf.write(os.path.join(root, file), arcname=file)
    memory_file.seek(0)
    return send_file(memory_file, mimetype='application/zip', as_attachment=True, download_name='ebay_images.zip')

def download_ebay_listing_images(ebay_url):
    response = requests.get(ebay_url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    image_urls = set(re.findall(r'(https://i\.ebayimg\.com/images/g/[A-Za-z0-9\-_]+/s-l1600\.(jpg|png))', soup.prettify()))
    image_urls = {match[0] for match in image_urls}
    
    downloaded_files = []
    for index, url in enumerate(image_urls, start=1):
        file_extension = url.split('.')[-1]
        file_name = f"image_{index}.{file_extension}"
        image_response = requests.get(url)
        image_response.raise_for_status()
        
        image_path = os.path.join(IMAGES_DIR, file_name)
        if not os.path.exists(IMAGES_DIR):
            os.makedirs(IMAGES_DIR)
        with open(image_path, 'wb') as file:
            file.write(image_response.content)
        downloaded_files.append(file_name)
    
    return downloaded_files

if __name__ == "__main__":
    app.run(debug=True)