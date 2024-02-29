from flask import Flask, render_template, request
import cv2
import pytesseract
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# pytesseract.pytesseract.tesseract_cmd = r'<Your Tesseract-OCR installation path>'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            image_path = None  # 初始化圖片路徑為 None
            if plate_number == "NBX-5588\n":
                name = "A owner"
                image_path = "static/Aowner.jpg"
            elif plate_number == "ABC-5678\n":
                name = "B owner"
                image_path = "static/Bowner.jpg"

            # 使用 render_template 渲染結果頁面，並傳遞車牌號碼、車主名稱和車主圖片路徑
            return render_template('result.html', plate_number=plate_number.strip(), name=name, image_path=image_path)
    return '''
    <!doctype html>
    <title>Upload license plate</title>
    <h1>Upload license plate image for recognition</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
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
