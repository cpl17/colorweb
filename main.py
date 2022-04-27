from flask import Flask,render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

from wtforms.fields import IntegerField, FileField, SubmitField
from wtforms.validators import DataRequired

import os
from werkzeug.utils import secure_filename


import numpy as np
from colorthief import ColorThief
from matplotlib.colors import to_hex


BASE_IMG_URL = "static\img\pexels-photo-1133957.jpeg"
NUM_COLORS = 10
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = "static/img"
app.config['SECRET_KEY'] = "secret"


class ImgInfo(FlaskForm):

    img = FileField("Image", validators=[DataRequired()])
    num = IntegerField("Number of Colors", validators=[DataRequired()])

    submit = SubmitField('Submit')


def get_colors(url, num):

    color_thief = ColorThief(url)
    top_colors = color_thief.get_palette(color_count=num) 
    top_colors_arr = np.array(top_colors) / 255
    top_colors_hex = [to_hex(color) for color in top_colors_arr]

    return top_colors_hex


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
    form = ImgInfo()
    colors = get_colors(BASE_IMG_URL,NUM_COLORS)
    return render_template('index.html',form=form)

@app.route('/', methods=['POST'])
def upload_image():

    form = ImgInfo()
   
    num_colors = request.form.get("num")

    if 'img' not in request.files:
        print('hello')
        return redirect(request.url)
    
    
    file = request.files['img']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = "static/img/" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if num_colors == None:

            num_colors = BASE_NUM_COLORS

        colors=get_colors(filepath,int(num_colors))

        return render_template('index.html', colors=colors,form=form)

    else:
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='static/img' + filename), code=301)

if __name__ == '__main__':
    app.run(debug=True)
