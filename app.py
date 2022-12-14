import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img
import tensorflow as tf

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


batch_size = 32
img_height = 224
img_width = 224


app = Flask(__name__)
app.secret_key = "secret key1"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
testing='static/uploads/test.png'

def allowed_file(filename): 
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    file.filename = "test.png"
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')

            # Loading the Model
        savedModel = load_model('cancerModel.h5')
        savedModel.summary()

        
        img1=load_img(testing)
        img1=img1.resize((img_height, img_width))
        input_arr = tf.keras.preprocessing.image.img_to_array(img1)
        img = input_arr.reshape( -1,224, 224,3)
        img.shape

        return render_template('index.html', filename=filename)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run()
