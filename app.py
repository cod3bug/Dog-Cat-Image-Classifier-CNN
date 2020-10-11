from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods = ["POST"])
def predict():
    message = request.form["img-url"]
    try:
        img_data = requests.get(message).content
        with open('./static/image_name.jpg', 'wb') as handler:
            handler.write(img_data)
        picFolder = os.path.join('./static')
        pic = "image_name.jpg"
        app.config['UPLOAD_FOLDER'] = picFolder
        img = os.path.join(app.config['UPLOAD_FOLDER'], pic)
        from keras.models import load_model
        model = load_model('./model.h5')
        import numpy as np
        from keras.preprocessing import image
        pro_img = './static/image_name.jpg'
        test_image = image.load_img(pro_img, target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict(test_image)
        if result[0][0] == 1:
            prediction = 'Dog'
        else:
            prediction = 'Cat'
        return render_template("index.html", disp_img=img, prediction=prediction)
    except:
        return render_template("index.html", disp_img=img, prediction="Error While Processing the Image URL")
    # img_data = requests.get(message).content
    # with open('./static/image_name.jpg', 'wb') as handler:
    #     handler.write(img_data)

if __name__ == "__main__":
    app.run(debug=True)