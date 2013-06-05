# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.contrib.fixers import ProxyFix
from module import classify, extractor, imageprocess, qna
import os


UPLOAD_FOLDER = "db"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


MrLee = Flask(__name__)
MrLee.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MrLee.wsgi_app = ProxyFix(MrLee.wsgi_app)


## Main Page
@MrLee.route("/")
def main():
    return render_template("main.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


## POST API
@MrLee.route("/process", methods=['POST'])
def process():
    error = None
    if request.method == 'POST':
        if request.form['action'] == "text":
            contents = request.form['contents']
            returnee = {
                "class": classify.do(contents).split()[0],
                "keyword": extractor.extract(contents)
            }
            return jsonify(returnee)

        elif request.form['action'] == "qna":
            returnee = {
                "answer": qna.quest(request.form['contents'])
            }
            return jsonify(returnee)

        elif request.form['action'] == "image":
            image = request.files['image']
            returnee = {}
            if image and allowed_file(image.filename):
                fullpath = os.path.join(MrLee.config['UPLOAD_FOLDER'], image.filename)
                image.save(fullpath)

                returnee = {
                    "uploaded": fullpath,
                    "inspected": imageprocess.do(os.path.abspath(fullpath))
                }
            return jsonify(returnee)

        else:
            error = "Invalid action inserted."

    return error


## Get Images
@MrLee.route("/db/<filename>", methods=['GET'])
def uploaded(filename):
    return send_file(os.path.join(MrLee.config['UPLOAD_FOLDER'], filename))


if __name__ == "__main__":
    MrLee.run(debug=True, port=8000)