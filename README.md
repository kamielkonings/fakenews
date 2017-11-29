## Fake news site

https://fakenewsgetr.herokuapp.com/

# Tech

* Python
* Flask
* Pattern (Python Library for natural language parsing)
* Heroku
* GitHub

# Installation (macOS)

    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

# Installation (Windows)

    pip install virtualenv
    virtualenv venv
    venv\Scripts\activate.bat
    pip install -r requirements.txt

# Running the server (macOS)

    source venv/bin/activate
    python server.py

# Running the server (Windows)

    venv\Scripts\activate.bat
    python server.py

# Fetching fake news

    source venv/bin/activate
    python fakenews.py fetch

# Deploy to Heroku

    git push
