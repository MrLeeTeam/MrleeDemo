# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, jsonify
from module import classify, extractor

MrLee = Flask(__name__)


@MrLee.route("/")
def main():
    return render_template("main.html")


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

            return "hi"
        else:
            error = "Invalid action inserted."

    return error


if __name__ == "__main__":
    MrLee.run(debug=True)