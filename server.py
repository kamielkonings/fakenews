import os
from flask import Flask, render_template

from fakenews import do_generate

app = Flask(__name__)


@app.route("/")
def homepage():
    items = do_generate()

    return render_template('homepage.html', items=items)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
