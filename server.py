# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.contrib.fixers import ProxyFix
from module import classify, extractor
import os


UPLOAD_FOLDER = "db"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


MrLee = Flask(__name__)
MrLee.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MrLee.wsgi_app = ProxyFix(MrLee.wsgi_app)


@MrLee.route("/")
def main():
    return render_template("main.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@MrLee.route("/process", methods=['POST'])
def process():
    error = None
    returnee = {}
    if request.method == 'POST':
        if request.form['action'] == "text":
            contents = request.form['contents']

            returnee = {
                "class": classify.do(contents).split()[0]
            }

            returnee["keyword"] = extractor.extract(contents)

            return jsonify(returnee)

        elif request.form['action'] == "image":
            return "kk"
            # image = request.files['image']
            # if image and allowed_file(image.filename):
            #     image.save(os.path.join(MrLee.config['UPLOAD_FOLDER'], image.filename))
            #
            #     return url_for("db", filename=image.filename)

        else:
            error = "Invalid action inserted."

    return error


if __name__ == "__main__":
    MrLee.run(debug=True, port=8000)