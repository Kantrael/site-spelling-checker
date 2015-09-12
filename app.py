# coding=utf-8
from flask import Flask, render_template, json, request

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    # read the posted values from the UI
    _url = request.form['inputUrl']

    # validate the received values
    if _url:
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


if __name__ == "__main__":
    app.run()
