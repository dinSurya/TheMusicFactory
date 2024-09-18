#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for, abort, request, flash, session
from flask_sqlalchemy import SQLAlchemy

import random, math

# from .data import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musicfactory.db'
db = SQLAlchemy(app)

app.secret_key = "musicalpippin2024"

types_list = [
    "Identifying Chords (Reading)",
    "Reading the Staff",
    "Defining Terms",
    "Transcribing Melodies",
    "Identifying Chords (Listening)",
    "Identifying Key Signatures",
    "Identifying Note Lengths"
]

class Types(db.Model):
    __tablename__ = "qTypes"
    type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    questions = db.relationship("Question", backref=db.backref("qTypes"))

class Question(db.Model):
    __tablename__ = "questions"
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    type_id = db.Column(db.Integer, db.ForeignKey('qTypes.type_id'))

db.create_all()

@app.route("/")
def home_page():
    q_list = Question.query.all()
    return render_template("home.html", qList=q_list)

@app.route("/quizzes")
def quiz_page():
    return render_template("quizzes.html")

@app.route("/lessons")
def lesson_page():
    type_list = Types.query.all()
    return render_template("lessons.html", tList=type_list)

@app.route('/data-form', methods=['POST', 'GET'])
def data_form():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        type_id = int(request.form['qType'])
        type_obj = Types.query.get(type_id)
        new_question = Question(question=question, answer=answer, qTypes=type_obj)
        db.session.add(new_question)
        db.session.commit()
    type_data = Types.query.all()
    q_list = Question.query.all()
    return render_template("dataform.html", tList=type_data, qList=q_list)

@app.route('/insert-data')
def dummy_data():
    type_data = Types.query.all()
    if not len(type_data):
        type1 = Types(name=types_list[0])
        type2 = Types(name=types_list[1])
        type3 = Types(name=types_list[2])
        type4 = Types(name=types_list[3])
        type5 = Types(name=types_list[4])
        type6 = Types(name=types_list[5])
        type7 = Types(name=types_list[6])
        db.session.add_all([type1, type2, type3, type4, type5, type6, type7])

        question_data = Question.query.all()
        if not len(question_data):
            q1 = Question(question="What is this note in the treble clef?", answer="F", qTypes=type2)
            q2 = Question(question="What type of chord is this?", answer="A Major", qTypes=type1)
            q3 = Question(question="What is a fermata?", answer="a symbol over a musical note or notes on sheet music indicates the notes can be held longer according to the conductor or soloist", qTypes=type3)
            q4 = Question(question="Finish the melody (starting note given)", answer="", qTypes=type4)
            q5 = Question(question="What type of chord is this?", answer="C Minor", qTypes=type5)
            q6 = Question(question="What key is this?", answer="D Major", qTypes=type6)
            q7 = Question(question="How many beats is this note?", answer="2", qTypes=type7)
            q8 = Question(question="What is this note in the bass clef?", answer="B", qTypes=type2)
            db.session.add_all([q1, q2, q3, q4, q5, q6, q7, q8])

        db.session.commit()

    return redirect(url_for('home_page'))