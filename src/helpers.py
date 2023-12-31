import os
from werkzeug.utils import secure_filename
from flask import current_app
import secrets  

# function which will help to save the uploaded images in static/images folder
def save_image(image, upload_folder='static/images', name=None):
    if image:
        filename = secure_filename(image.filename)
        if name:
            filename = name + filename
        filepath = os.path.join(current_app.root_path, upload_folder, filename)
        image.save(filepath)
        return filename
    return None
