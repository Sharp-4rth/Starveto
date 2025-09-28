# Starveto 🍽️

Starveto is a Flask web application that helps users find the fastest restaurants near their postcode.

---

## Features
- User authentication (login, register, sessions)
- Save and display user postcode
- Form validation with Flask-WTF

---

## Requirements
Python 3.12+  
Flask and other dependencies (see `requirements.txt`)

---

## Configuration
A default `SECRET_KEY` is provided in `config.py` for development purposes.  
For production, you should override it by setting a `SECRET_KEY` environment variable in `.flaskenv` or your deployment config:

---

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/starveto.git
   cd starveto
   
---

## Project structure

    starveto/
    │── app/                 # Main Flask app
    │   ├── __init__.py      # App factory / setup
    │   ├── models.py        # Database models
    │   ├── views.py         # Route handlers
    │   ├── forms.py         # Flask-WTF forms
    │   ├── templates/       # HTML templates
    │   └── static/          # CSS, JS, images
    │
    ├── requirements.txt     # Python dependencies
    ├── package.json         # Node dependencies (if using)
    ├── run.py               # Entry point
    └── README.md            # Project documentation

---

## Contributing
Pull requests are welcome! Please open an issue first to discuss changes.