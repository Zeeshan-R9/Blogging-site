from flask import render_template
from flask_mail import Message
from . import mail
from .auth import auth

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to], sender='zeeshanrabnawaz9@gmail.com')

    msg.body = render_template(f"{template}.txt", **kwargs)
    msg.html = render_template(f"{template}.html", **kwargs)

    sent = False
    while not sent:
        try:
            mail.send(msg)
            sent = True
        except Exception:
            pass