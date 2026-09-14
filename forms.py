from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


class LetterForm(FlaskForm):
    recipient_name = StringField(
        "Recipient Name",
        validators=[DataRequired()]
    )

    recipient_email = StringField(
        "Recipient Email",
        validators=[DataRequired(), Email()]
    )

    subject = StringField(
        "Subject",
        validators=[DataRequired()]
    )

    body = TextAreaField(
        "Letter",
        validators=[DataRequired()]
    )

    save = SubmitField("Save Draft")
    send = SubmitField("Send Letter")