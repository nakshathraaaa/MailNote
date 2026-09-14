# MailNote ✉️

### Write. Save. Send.

MailNote is a simple Flask web application for writing, saving, editing, and sending letters through email.

## Features

- Write a new letter
- Save letters as drafts
- View saved letters
- Edit draft letters
- Send letters through email using Flask-Mail
- Delete letters
- Form validation using Flask-WTF
- Database management using Flask-SQLAlchemy
- Database migrations using Flask-Migrate
- Asynchronous email sending using a background thread

## Technologies Used

- Python
- Flask
- Flask-Mail
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- Jinja2
- HTML
- CSS

## Project Structure

```text
MailNote/
│
├── app.py
├── forms.py
├── models.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── compose.html
│   ├── letters.html
│   └── edit.html
│
├── static/
│   └── style.css
│
└── migrations/
