import json
from flask import Flask, render_template, flash, redirect, url_for, request
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'I8Is25DFOzLUKSx06WCyesvHJgmZJblt'


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # todo call API to create new user
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    return render_template("login.html", title='Login', form=form)


@app.route('/dashboard/<company_name>')
def dashboard(company_name):
    return render_template("dashboard.html", company_name=company_name)


@app.route('/engagements/<engagement_name>', methods=['GET', 'POST', 'PUT'])
def engagements(engagement_name):
    return render_template("engagement.html", engagement_name=engagement_name)


@app.route('/position', methods=['GET', 'POST', 'PUT'])
def position(position_name):
    return render_template("position.html", position_name=position_name)


@app.route('/profile', methods=['GET', 'POST', 'PUT'])
def profile():
    return render_template("profile.html")


if __name__ == '__main__':
    app.run(debug=True)
