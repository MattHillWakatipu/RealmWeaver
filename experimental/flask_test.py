from flask import Flask, render_template, request

import realm_weaver

app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    response = realm_weaver.main(user_text)
    return response


if __name__ == "__main__":
    app.run()
