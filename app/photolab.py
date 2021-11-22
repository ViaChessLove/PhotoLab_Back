# -*- coding: utf-8 -*-
from datetime import datetime
import smtplib 
from email.mime.text import MIMEText 
 
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/reviews'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photolab_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#reviews = []


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return f"<reviews {self.id}"

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(200), nullable=False)
    def __repr__(self):
        return f"<emails {self.id}"

@app.route('/', methods=['GET'])
@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', reviews = Review.query.all())

@app.route('/add_message', methods=['POST'])
def add_message():
    #text = request.form['review_text'] + 3*"\t" + str(datetime.now())
    #reviews.append(text)
    rev = Review(review_text = request.form['review_text'])
    db.session.add(rev)
    db.session.commit()
    return redirect(url_for('main'))

@app.route('/send_email', methods=['POST'])
def send_email():
    sender = "photolab.website.susu@gmail.com"
    passcode ="susu123photolab"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender, passcode)
    message = "Здравствуйте, это автоответчик Photolab. В ближайшее время с вами свяжется наш сотрудник"
    msg = MIMEText(message)
    msg["Subject"] = "PHOTOLAB"
    email = request.form['email']
    em = Email(mail = email)
    db.session.add(em)
    db.session.commit()
    server.sendmail(sender, email, msg.as_string())
    return render_template('main.html')



@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
'''
# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123@localhost/reviews_db'
db = SQLAlchemy(app)


#reviews = []
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.String(1024), nullable=False)

    def __init__(self, review_text):
        self.review_text = review_text

db.create_all()

@app.route('/', methods=['GET'])
@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', reviews = Review.query.all())

@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['review_text'] + "\t" + " at " + str(datetime.now())
    db.session.add(text)
    db.session.commit()

    return redirect(url_for('main'))
'''