from flask import Flask,request, url_for, redirect, render_template
from werkzeug.utils import secure_filename
import requests
import json
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/getplate", methods=['GET', 'POST'])
def getno():
    if request.method == 'POST':
        plate = request.files['plate']
        filename = secure_filename(plate.filename)
        upload = plate.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        regions = ['in']
        with open('static/uploads/'+filename, 'rb') as fp:
            response = requests.post('https://api.platerecognizer.com/v1/plate-reader/', data=dict(regions=regions), files=dict(upload=fp), headers={'Authorization': 'Token 7c9ced42ce6ac2938556d5a4e8c52422ad1b5cea'})
        data = response.json()
        for plate in data['results']:
            plate_data = plate['plate']
            score = plate['score']
            score = score*100

        file_success = "Number Plate : "+plate_data+" with a probability of "+str(score)+"%"
        return render_template("upload.html", file_success=file_success)
    else:
        error = "Process Failed"
        return render_template("upload.html", error=error)


if __name__ == '__main__':
    app.run(debug=True)
