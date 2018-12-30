from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm
from jobex_web_app_helper import JobexWebHelper
from config_helper import ConfigHelper
from Classes import user, login
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

config = ConfigHelper('jobex-web-app/Configurations.ini')
rest_host = config.readRestParams('REST_HOST')
jobex_web_helper = JobexWebHelper(host=rest_host)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'I8Is25DFOzLUKSx06WCyesvHJgmZJblt'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_view'
login_manager.login_message_category = 'info'


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_obj = user.User(username=form.username.data, email=form.email.data, password=hashed_password)
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
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        login_obj = login.Login(email=email, password=hashed_password)
        try:
            response = jobex_web_helper.login(login_obj)
            username = response.content
            if response.status_code == 200:
                login_user(username, remember=form.remember.data)
                return redirect(url_for('dashboard'))
            else:
                flash(f'Login unsuccessful! please check email and password', 'warning')
        except IOError as err:
            flash(f'Login call failed for {form.email.data}! Error = ' + str(err), 'warning')

    return render_template("login.html", title='Login', form=form)


@app.route('/logout')
def logout_view():
    logout_user()
    return redirect(url_for('home'))


@app.route('/dashboard/<company_name>')
@login_required
def dashboard(company_name):
    positions = jobex_web_helper.get_all_positions(company_name=company_name)
    return render_template("dashboard.html", positions=positions)


@app.route('/engagements/<engagement_name>', methods=['GET', 'POST', 'PUT'])
@login_required
def engagements(engagement_name):
    return render_template("engagement.html", engagement_name=engagement_name)


@app.route('/position', methods=['GET', 'POST', 'PUT'])
@login_required
def position(position_name):
    return render_template("position.html", position_name=position_name)


@app.route('/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    return render_template("profile.html")


if __name__ == '__main__':
    if config.readAppSettings(Key='ServerDebug') == '1':
        app.debug = True
    app.run(port=5051)
