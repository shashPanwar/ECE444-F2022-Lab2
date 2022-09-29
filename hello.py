from ensurepip import bootstrap
from datetime import datetime
from flask import Flask, render_template, session, redirect, flash, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'pass777'

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email Address?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index(): 
    # return render_template('index.html', current_time = datetime.utcnow())
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data

        return redirect(url_for('index'))

    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time = datetime.utcnow())

if __name__ == '__main__':
    app.run(debug=True)