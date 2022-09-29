from ensurepip import bootstrap
from datetime import datetime
from flask import Flask, render_template, session, redirect, flash, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
# import email


app = Flask(__name__)
app.config['SECRET_KEY'] = 'pass777'

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email Address?', validators=[Email()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index(): 
    # return render_template('index.html', current_time = datetime.utcnow())
    name = None
    form = NameForm()

    # email_form = NameEmailForm()

    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data

        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your name!')
        session['email'] = form.email.data

        if 'utoronto' in session['email']:
            session['uoft'] = True
        else:
            session['uoft'] = False
            
        return redirect(url_for('index'))

    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), uoft = session.get('uoft'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time = datetime.utcnow())

if __name__ == '__main__':
    app.run(debug=True)