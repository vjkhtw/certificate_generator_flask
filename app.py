from flask import Flask, render_template, request, json, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from PIL import Image, ImageFont, ImageDraw
from flask_mail import Mail, Message
import os
import cv2 as cv
import openpyxl

upload_folder = "static/media/"
csv_folder = "static/csv/details.xlsx"
IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif']

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
app.config['IMAGE_TYPES'] = IMAGE_TYPES

app.config['MAIL_SERVER'] = 'smtp.zoho.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'emailaddress'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)

if not os.path.exists(csv_folder):
    os.mkdir(csv_folder)

app.config['UPLOAD_FOLDER'] = upload_folder

class UploadFileForm(FlaskForm):
    file = FileField("File", validators= [InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods = ['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = request.files['file']
        filename  = secure_filename(file.filename)
        if file.mimetype not in app.config['IMAGE_TYPES']:
            return("File Type not allowed!!")
        file.save(os.path.join(upload_folder, file.filename))
        print("File Uploaded Successfully!!")
        return render_template("preview.html", filename = filename)  
    return render_template("index.html", form = form)

@app.route("/coordinates/<string:data>", methods = ['POST'])
def coordinates(data):
    coordinates = json.loads(data)
    x_cord = coordinates['x']
    y_cord = coordinates['y']
    name = coordinates['name']
    print(x_cord, y_cord, name) 
    return redirect(url_for("process", x = x_cord, y = y_cord, name = name)) 

@app.route("/process/<string:name>/<int:x>/<int:y>")
def process(name, x, y):
    template_path = upload_folder + name
    output_path = "static/output/"
    font_size = 50
    font_color = (0,0,0)
    obj = openpyxl.load_workbook(csv_folder)
    sheet = obj.active
    for i, row in enumerate(sheet.iter_rows(values_only=True), start=1):
        certi_name = row[0]
        email_addr = row[1]
        img = Image.open(template_path)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", font_size)
        draw.text((x, y), certi_name, font=font, fill=font_color)
        certi_path = os.path.join(output_path, f"certi{i}.png")
        img.save(certi_path)
        msg = Message('Hello', sender = 'emailaddress', recipients = [email_addr])
        msg.body = f"Hello {certi_name}, this is a flask message sent from Flask-Mail"
        with app.open_resource(certi_path) as fp:
            msg.attach(certi_path, "image/png", fp.read())
        mail.send(msg)
    return "Success!"

if __name__ == "__main__":
    app.run(debug = True)