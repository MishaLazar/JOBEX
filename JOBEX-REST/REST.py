from flask import Flask, jsonify, redirect, url_for, render_template, flash, session, request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_cors import CORS
from JobThread import JobThread
from Utils.config_helper import ConfigHelper
from Controllers.mobile_controller import MobileController
from Controllers.web_controller import WebController
from Controllers.resources_controller import ResourcesController
from Controllers.auth_controller import AuthController
from Utils.json_encoder import JSONEncoder
# from jobs_service import JobThread
from Utils.util import Utils
from forms import RegistrationForm, LoginForm, AddPositionForm
import json

app = Flask(__name__)

config = ConfigHelper.get_instance()
app.config['SECRET_KEY'] = config.read_auth('SECRET_KEY')   # 'I8Is25DFOzLUKSx06WCyesvHJgmZJblt'
app.config['JWT_SECRET_KEY'] = config.read_auth('SECRET_KEY')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True)
CORS(app)
jwt = JWTManager(app)


# Web page routes

@app.route('/')
def home_view():
    return render_template("home.html")


@app.route("/about")
def about_view():
    return render_template('about.html', title='About')


@app.route('/register_view')
def register_view():
    form = RegistrationForm()
    return render_template("register.html", title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()
    return render_template("login.html", title='Login', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout_view():
    # todo replace this with JS code
    return redirect(url_for('home_view'))


@app.route('/dashboard')
def dashboard_view():
    return render_template("dashboard.html", authenticated=True)


@app.route('/add_position', methods=['GET', 'POST'])
def add_position_view():
    form = AddPositionForm()
    return render_template("add_position.html", title='Add Position', form=form, authenticated=True)


@app.route('/engagements')
def engagement_view():
    return render_template("engagement.html", authenticated=True)


@app.route('/position_view')
def position_view():
    return render_template("position.html", authenticated=True)


@app.route('/profile')
def profile_view():
    return render_template("profile.html", authenticated=True)


# API routes

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return AuthController.check_token_in_blacklist(jti)


@app.route('/logout/<token_type>', methods=['POST'])
def logout_user(token_type):
    if request.method == 'POST':
        if token_type == "access":
            return redirect(url_for('logout_access'))
        if token_type == "refresh":
            return redirect(url_for('logout_refresh'))


@app.route('/logout_access_token')
@jwt_required
def logout_access():
    if request.method == 'POST':
        jti = get_raw_jwt()['jti']
    return AuthController.add_token_to_blacklist(jti)


@app.route('/logout_refresh_token')
@jwt_refresh_token_required
def logout_refresh():
    if request.method == 'POST':
        jti = get_raw_jwt()['jti']
    return AuthController.add_token_to_blacklist(jti)


@app.route('/get_login', methods=['POST'])
def get_login():
    if request.method == 'POST':
        authentication = json.loads(request.get_json())
        username = authentication['username']
        password = authentication['password']
        result = None

        try:
            result = AuthController.login(username, password)
        except IOError as err:
            print("Failed to login. Error: {}".format(err))

        if result:
            access_token = create_access_token(identity=result)
            refresh_token = create_refresh_token(identity=result)
            data = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            return jsonify(data), 200
        else:
            return jsonify({"message": "Wrong credentials"}), 403
    else:
        return jsonify({'message': 'Method not supported'}), 500


@app.route('/tokenRefresh', methods=['POST'])
@jwt_refresh_token_required
def get_refreshed_token():
    if request.method == 'POST':
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        return jsonify({
                'access_token': access_token
               }), 200
    else:
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/checkAuthenticationStatus', methods=['POST'])
@jwt_required
def get_authentication_status():
    if request.method == 'POST':
        return jsonify({'message': 'you are authenticated!'}), 200


@app.route('/putWithAuth', methods=['POST'])
def put_object_with_auth():
    if request.method == 'POST':
        obj = request.get_json()
        mob_ctrl = MobileController.get_instance()
        result = {
            "inserted_id": str(mob_ctrl.create_obj_with_authentication(obj))
        }
        return jsonify(result)


# @app.route('/getStudentEngagements/<student_Id>')
# def get_student_engagements(student_id):
#     mob_ctrl = MobileController.get_instance()
#     result = mob_ctrl.get_StudentEngagements(studentId=student_id)
#     return result


@app.route('/create_employee', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.values

        return jsonify(user)
    else:
        user = request.args.get_json()
        return jsonify(user)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        user = request.get_json()
        web_ctrl = WebController.getInstance()
        new_user = web_ctrl.add_user(user)
        if new_user:
            return jsonify({'result': 'success'}), 200
    else:
        return jsonify({'message': 'Method not supported'}), 500


@app.route('/positions/<position_id>', methods=['POST', 'GET'])
@app.route('/positions', methods=['POST', 'GET'])
def positions(position_id=None):
    if request.method == 'POST':
        position = request.get_json()
        web_ctrl = WebController.getInstance()
        result = {"position_id": str(web_ctrl.add_position(position))}
        return jsonify(result)
    elif request.method == 'GET':
        web_ctrl = WebController.getInstance()
        if position_id:
            result = web_ctrl.get_positions(position_id=position_id)
        else:
            result = web_ctrl.get_positions()
        return JSONEncoder().encode(result)
    else:
        return {"error": "method {} not supported!".format(request.method)}


@app.route('/engagements/<company_name>/<engagement_id>', methods=['POST', 'GET'])
def engagements(company_name=None, engagement_id=None):
    if request.method == 'POST':
        engagement = request.get_json()
        web_ctrl = WebController.getInstance()
        result = {"engagement_id": str(web_ctrl.add_engagement(engagement))}
        return jsonify(result)
    elif request.method == 'GET':
        web_ctrl = WebController.getInstance()
        if company_name and engagement_id:
            result = web_ctrl.get_engagements(company_name=company_name, engagement_id=engagement_id)
        elif company_name:
            result = web_ctrl.get_engagements(engagement_id=engagement_id)
        return JSONEncoder().encode(result)
    else:
        return {"error": "method {} not supported!".format(request.method)}


@app.route('/resources/skills/skill=<skill_to_find>', methods=['GET'])
@app.route('/resources/skills', methods=['POST', 'GET'])
def skills(skill_to_find=None):
    res_control = ResourcesController.get_instance()
    if request.method == 'POST':
        result = res_control.add_skill(request.get_json())
    elif request.method == 'GET':
        if skill_to_find:
            result = res_control.search_skills(skill_to_find)
        else:
            result = res_control.get_all_skills()

    return JSONEncoder().encode(result)


@app.route('/student/getStudentEngagements/<student_Id>')
def get_student_engagements(student_id):
    mob_ctrl = MobileController.get_instance()
    result = mob_ctrl.get_StudentEngagements(studentId=student_id)
    return result


@app.route('/student/skills/<student_id>', methods=['POST', 'GET'])
def get_student_skills(student_id):
    result = None
    if request.method == 'POST':
        result = MobileController.get_student_skills(student_id)
    if request.method == 'GET':
        result = MobileController.get_student_skills(student_id)

    return JSONEncoder().encode(result)


@app.route('/matches/position_id=<position_id>', methods=['GET'])
@app.route('/matches/student_id=<student_id>', methods=['GET'])
@app.route('/matches', methods=['GET'])
def matches(student_id=None, position_id=None):
    if request.method == 'GET':
        web_ctrl = WebController.getInstance()
        if position_id:
            result = web_ctrl.get_matches(position_id=position_id)
        elif student_id:
            result = web_ctrl.get_matches(student_id=student_id)
        else:
            result = web_ctrl.get_matches()
        return JSONEncoder().encode(result)
    else:
        return {"error": "method {} not supported!".format(request.method)}


if __name__ == '__main__':
    if config.read_app_settings(Key='ServerDebug') == '1':
        app.debug = True
    if config.read_app_settings(Key='RunMatchEngine') == '1':
        example = JobThread(interval=Utils.int_try_parse(config.read_job(Key='DELAY_INTERVAL'),20))

    app.run(port=5050, threaded=True)

