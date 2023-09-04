from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config["SECRET_KEY"] = "Let's GO"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route('/')
def home():
    """Opens home page for user"""
    
    return render_template('home.html', survey=survey)


@app.route('/begin', methods=["POST"])
def clear_session():
    """Clears session and restarts survey for user"""

    session["responses"] = []
    
    return redirect('questions/0')



@app.route('/questions/<int:ques>')
def questions(ques):
    """Shows questions of survey to user"""
    
    responses = session.get(RESPONSES_KEY)
    
    if len(responses) == len(survey.questions):
        return redirect('thankyou.html')
    if len(responses) != ques:
        flash('Please answer this question first')
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[ques].question
    choices = survey.questions[ques].choices
    
    return render_template('questions.html', question=question, choices=choices)


@app.route('/answer', methods=["POST"])
def add_answer():
    """Saves user answers to responses"""
    
    answer = request.form["option"]
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses
    
    if len(responses) == len(survey.questions):
        return redirect('/thankyou')
    else:
        return redirect(f"/questions/{len(responses)}")
    

@app.route('/thankyou')
def thank_you():
    """Thanks user for taking survey"""
    
    return render_template('thankyou.html')