# License Plate Recognition

* This project is a Flask application designed for recognizing license plates from images. 
* It uses Docker to simplify deployment and environment setup. 
* Follow the instructions below to get started.

# Setup by venv

```bash
git clone https://github.com/Elmo-Lin/license_plate_recognition.git
```
```bash
.\test\Scripts\activate
```
```bash
pip install Flask opencv-python-headless pytesseract
```
```bash
python app.py
```
# Setup by docker

```bash
git clone https://github.com/Elmo-Lin/license_plate_recognition.git
```
```bash
cd license_plate_recognition
```
```bash
docker build -t license-plate-recognition .
```
```bash
docker run -p 5000:5000license-plate-recognition
```

