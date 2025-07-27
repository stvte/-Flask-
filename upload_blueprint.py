import datetime

from pathlib import Path

from flask import Blueprint, request, url_for, send_from_directory
from flask_ckeditor import upload_fail, upload_success

upload_blue = Blueprint('upload_blue','__name__')
PROJECT_ROOT = Path(__file__).parent.parent
UPLOAD_DIR = PROJECT_ROOT / "static/uploaded"

@upload_blue.route('/files/<path:filename>')
def uploaded_files(filename):
    save_path = UPLOAD_DIR
    return send_from_directory(save_path, filename)

@upload_blue.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')

    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename=timestamp+'.'+extension
    save_path=UPLOAD_DIR / filename
    f.save(str(save_path))
    url = url_for('upload_blue.uploaded_files', filename=filename)
    return upload_success(url=url)
