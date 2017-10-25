from flask import Flask, render_template

from fakenews import do_generate

app = Flask(__name__)


@app.route("/")
def homepage():
    items = do_generate()

    return render_template('homepage.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
