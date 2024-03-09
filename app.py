from flask import Flask, render_template, request
import cv2
import pytesseract
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)

# pytesseract.pytesseract.tesseract_cmd = r'<Your Tesseract-OCR installation path>'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
recognition_times = {}

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']

        if file.filename == '':
            return 'No selected file'
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            plate_number = recognize_license_plate(file_path)
            name = "Unknown"
            image_path = None  # Initialize image path as None

            current_time = datetime.now()
            interval = "首次停車"  # Assume first time parking if not found in records

            if plate_number in recognition_times:
                last_recognition_time = datetime.strptime(recognition_times[plate_number], "%Y-%m-%d %H:%M:%S")
                interval_seconds = (current_time - last_recognition_time).total_seconds()
                hours, remainder = divmod(interval_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                interval = f"{int(hours)}小時{int(minutes)}分鐘{int(seconds)}秒前"
            recognition_times[plate_number] = current_time.strftime("%Y-%m-%d %H:%M:%S")

            if plate_number == "NBX-5588\n":
                name = "A 車主"
                image_path = "static/Aowner.jpg"
            elif plate_number == "ABC-5678\n":
                name = "B 車主"
                image_path = "static/Bowner.jpg"
            elif plate_number == "BFQ-8888\n":
                name = "此車為贓車"
                image_path = "static/Cowner.jpg"

            # Pass interval instead of last_seen
            return render_template('result.html', plate_number=plate_number, name=name, image_path=image_path, last_seen=interval)
    return '''
    <!doctype html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>車牌辨識系統</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            padding: 20px;
            margin: 0;
        }

        h1 {
            color: #333;
            text-align: center;
        }

        form {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            margin: auto;
        }

        input[type="file"] {
            border: 1px solid #ddd;
            padding: 10px;
            width: calc(100% - 22px);
            margin-bottom: 20px;
        }

        input[type="submit"] {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }

        input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <h1>車牌辨識系統</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="上傳">
    </form>
</body>
</html>
    '''

def recognize_license_plate(img_path):
    image = cv2.imread(img_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    custom_config = r'--oem 3 --psm 6'
    plate_number = pytesseract.image_to_string(gray_image, config=custom_config)
    return plate_number

if __name__ == '__main__':
    app.run(debug=True)