from flask import Flask, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_mail import Mail, Message
from forms import LetterForm
from models import db, Letter

import threading
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "secret-key")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mailnote.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")


db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/compose", methods=["GET", "POST"])
def compose():
    form = LetterForm()

    if form.validate_on_submit():

        letter = Letter(
            recipient_name=form.recipient_name.data,
            recipient_email=form.recipient_email.data,
            subject=form.subject.data,
            body=form.body.data
        )

        db.session.add(letter)
        db.session.commit()

        if form.send.data:

            def send_email():
                with app.app_context():
                    message = Message(
                        subject=letter.subject,
                        recipients=[letter.recipient_email],
                        body=f"""
Dear {letter.recipient_name},

{letter.body}

Regards,
MailNote
"""
                    )

                    mail.send(message)

            threading.Thread(target=send_email).start()

            letter.status = "Sent"
            db.session.commit()

            flash("Letter sent successfully!")

        else:
            flash("Draft saved successfully!")

        return redirect(url_for("letters"))

    return render_template("compose.html", form=form)


@app.route("/letters")
def letters():
    letters = Letter.query.all()
    return render_template("letters.html", letters=letters)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    letter = Letter.query.get_or_404(id)

    form = LetterForm(obj=letter)

    if form.validate_on_submit():

        letter.recipient_name = form.recipient_name.data
        letter.recipient_email = form.recipient_email.data
        letter.subject = form.subject.data
        letter.body = form.body.data

        db.session.commit()

        flash("Letter updated successfully!")

        return redirect(url_for("letters"))

    return render_template("edit.html", form=form)

@app.route("/send/<int:id>", methods=["POST"])
def send_letter(id):
    letter = Letter.query.get_or_404(id)

    def send_email():
        with app.app_context():
            message = Message(
                subject=letter.subject,
                recipients=[letter.recipient_email],
                body=f"""
Dear {letter.recipient_name},

{letter.body}

Regards,
MailNote
"""
            )

            mail.send(message)

    threading.Thread(target=send_email).start()

    letter.status = "Sent"
    db.session.commit()

    flash("Letter sent successfully!")

    return redirect(url_for("letters"))

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    letter = Letter.query.get_or_404(id)

    db.session.delete(letter)
    db.session.commit()

    flash("Letter deleted successfully!")

    return redirect(url_for("letters"))


if __name__ == "__main__":
    app.run(debug=True)