from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm
from jobex_web_app_helper import JobexWebHelper
from config_helper import ConfigHelper
from flask_login import LoginManager, login_user

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
def home_view():
    dummy_positions = [['DevOps Engineer', 'R&D', 'Tel Aviv', 'Automation, Python', 'Yes', 'None'],
                 ['Software Engineer', 'R&D', 'Ramat Gan', 'Java, C#', 'No', 'Missing info']]
    return render_template("home.html", dummy_positions=dummy_positions)


@app.route("/about")
def about_view():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register_view():
    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_obj = {"username": form.username.data, "email": form.email.data, "password": hashed_password}
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
    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        login_obj = {"email": email, "password": hashed_password}
        try:
            response = jobex_web_helper.login(login_obj)
            company_name = response.to_json_str['company_name']
            if response.status_code == 200:
                login_user(email, remember=form.remember.data)
                return redirect(url_for('dashboard/{}'.format(company_name)))
            else:
                flash(f'Login unsuccessful! please check email and password', 'warning')
        except IOError as err:
            flash(f'Login call failed for {form.email.data}! Error = ' + str(err), 'warning')

    return render_template("login.html", title='Login', form=form)


@app.route('/logout')
def logout_view():
    # todo logout here
    return redirect(url_for('home_view'))


@app.route('/dashboard/<company_name>')
def dashboard_view(company_name):
    dashboard_positions = jobex_web_helper.get_all_positions(company_name=company_name)
    return render_template("dashboard.html", dashboard_positions=dashboard_positions)


@app.route('/engagements/<company_name>/<engagement_id>', methods=['GET', 'POST', 'PUT'])
def engagement_view(engagement_id, company_name):
    engagement = jobex_web_helper.get_engagement(company_name=company_name, engagement_id=engagement_id)
    return render_template("engagement.html", engagement=engagement)


@app.route('/positions/<company_name>/<position_id>', methods=['GET', 'POST', 'PUT'])
def position_view(company_name, position_id):
    position = jobex_web_helper.get_position(company_name=company_name, position_id=position_id)
    return render_template("position.html", position=position)


@app.route('/profile/<user_id>', methods=['GET', 'PUT'])
def profile_view(user_id):
    user = jobex_web_helper.get_user(user_id)
    return render_template("profile.html", user=user)


if __name__ == '__main__':
    if config.readAppSettings(Key='ServerDebug') == '1':
        app.debug = True
    app.run(port=5051)
