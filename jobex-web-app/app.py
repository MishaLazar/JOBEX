from flask import Flask, render_template, flash, redirect, url_for, session, request
from forms import RegistrationForm, LoginForm
from jobex_web_app_helper import JobexWebHelper
from config_helper import ConfigHelper
import json

config = ConfigHelper('jobex-web-app/Configurations.ini')
rest_host = config.readRestParams('REST_HOST')
jobex_web_helper = JobexWebHelper(host=rest_host)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'I8Is25DFOzLUKSx06WCyesvHJgmZJblt'


@app.route('/')
def home_view():
    return render_template("home.html")


@app.route("/about")
def about_view():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register_view():
    # todo check if authenticated then redirect to dashboard
    form = RegistrationForm()

    if form.validate_on_submit():
        user_obj = {"username": form.username.data, "email": form.email.data, "password": form.password.data}
        try:
            jobex_web_helper.create_user(user_obj)
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login_view'))
        except IOError as err:
            flash(f'Failed to create account for {form.username.data}! '
                  f'Please contact our support - support@jobex.com',
                  'warning')
            flash(f'Error = ' + str(err), 'info')

    return render_template("register.html", title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    # todo check if authenticated then redirect to dashboard
    form = LoginForm()

    if form.validate_on_submit():
        login_obj = {"username": form.username.data, "password": form.password.data}
        try:
            response = jobex_web_helper.login(login_obj)
            if response.status_code == 200:
                tokens = json.dumps(response.json())
                session['tokens'] = tokens
                session['username'] = form.username.data
                return redirect(url_for('save_tokens', tokens=tokens, username=form.username.data))
            else:
                flash(f'Login unsuccessful! please check email and password', 'warning')
        except IOError as err:
            flash(f'Login call failed for {form.username.data}! Error = ' + str(err), 'warning')

    return render_template("login.html", title='Login', form=form)


# this will save tokens in the browser and redirect to dashboard with the username
@app.route('/save_tokens')
def save_tokens():
    # todo how to block this route if it's not sourced by the server redirect?
    tokens = json.loads(request.args['tokens'])
    username = request.args['username']
    return render_template("save_tokens.html", tokens=tokens, username=username)


@app.route('/logout', methods=['GET', 'POST'])
def logout_view():
    # todo logout here
    return redirect(url_for('home_view'))


@app.route('/dashboard')
def dashboard_view():
    return render_template("dashboard.html", authenticated=True)


@app.route('/engagements/<engagement_id>')
def engagement_view(engagement_id):
    return render_template("engagement.html", authenticated=True)


@app.route('/positions/<position_id>')
def position_view(position_id):
    return render_template("position.html", authenticated=True)


@app.route('/profile')
def profile_view():
    return render_template("profile.html", authenticated=True)


if __name__ == '__main__':
    if config.readAppSettings(Key='ServerDebug') == '1':
        app.debug = True
    app.run(port=5051)
