from flask import Flask, jsonify, redirect, url_for, render_template, request  # ,flash, session
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from flask_cors import CORS

from Classes.match import Match
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
from werkzeug import exceptions
# import json

app = Flask(__name__)

config = ConfigHelper.get_instance()
app.config['SECRET_KEY'] = config.read_auth('SECRET_KEY')  # 'I8Is25DFOzLUKSx06WCyesvHJgmZJblt'
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
    return redirect(url_for('home_view'))


@app.route('/dashboard')
def dashboard_view():
    return render_template("dashboard.html", authenticated=True)


@app.route('/add_position', methods=['GET', 'POST'])
def add_position_view():
    form = AddPositionForm()
    return render_template("add_position.html", title='Add Position', form=form, authenticated=True)


@app.route('/engagement_view')
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
        authentication = request.get_json()
        username = authentication['username']
        password = authentication['password']
        result = None

        try:
            result = AuthController.login(username, password)
        except IOError as err:
            print("Failed to login. Error: {}".format(err))

        if result:
            access_token = create_access_token(identity=str(result["_id"]))
            refresh_token = create_refresh_token(identity=str(result["_id"]))
            data = {
                "username": result["username"],
                "company_id": str(result["company_id"]),
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            return jsonify(data), 200
        else:
            return jsonify({"message": "Wrong credentials"}), 403
    else:
        return jsonify({'message': 'Method not supported'}), 500


@app.route('/get_dashboard_main_chart_data', methods=['POST'])
@jwt_required
def get_dashboard_matches_for_charts():
    if request.method == 'POST':
        user_id = request.get_json()["user_id"]
        result = MobileController.get_dashboard_counters_for_main_chart(student_id=user_id)
        return jsonify(result), 200
    else:
        return jsonify({"message": "Oops ..."}), 403


@app.route('/get_student_profile', methods=['POST'])
@jwt_required
def get_student_profile():
    if request.method == 'POST':
        user_id = request.get_json()
        # mob_ctrl = MobileController()
        # data = mob_ctrl.get_student_profile(user_id['user_id'])
        data = MobileController.get_student_profile_and_skill(user_id['user_id'])[0]
        result = {
            "userId": str(data["_id"]),
            "firstName": data["firstName"],
            "lastName": data["lastName"],
            "email": data["email"],
            "username": data["username"],
            "userId": data["userId"],
            "address": data["address"],
            "profileImg": data["profileImg"],
            "active": data["active"],
            "activation_data": data["activation_data"],
            "creation_data": data["creation_data"],
            "student_skill_list": data["student_skills"]["student_skill_list"]
        }
        return jsonify(result), 200
    else:
        return jsonify({"message": "Wrong user_id"}), 403


@app.route('/register_student', methods=['POST'])
def register_student():
    if request.method == 'POST':
        user = request.get_json()
        mob_ctrl = MobileController()
        new_user_id = mob_ctrl.register_user(user)
        if new_user_id:
            access_token = create_access_token(identity=str(new_user_id))
            refresh_token = create_refresh_token(identity=str(new_user_id))
        return jsonify({
            'user_id': str(new_user_id),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    else:
        return jsonify({'message': 'Something went wrong'}), 500


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


@app.route('/activate_student_profile', methods=['POST'])
@jwt_required
def get_authentication_status():
    if request.method == 'POST':
        request_data = request.get_json()
        user_id = request_data['user_id']
        active_status = request_data['active_status']
        response = MobileController.set_active_status_on_profile(user_id, active_status)
        if bool(active_status):
            MobileController.set_student_for_rematch(user_id)
        return jsonify(response), 200


@app.route('/putWithAuth', methods=['POST'])
def put_object_with_auth():
    if request.method == 'POST':
        obj = request.get_json()
        mob_ctrl = MobileController()
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
        web_ctrl = WebController.getInstance()
        user = request.get_json()
        company_name = user['company_name']
        company_description = user['company_description']
        if company_name not in companies:
            company_id = web_ctrl.add_company(company_name, company_description)
            user["company_id"] = company_id
            companies.append(company_name)
        new_user = web_ctrl.add_user(user)
        if new_user:
            return jsonify({'result': 'success'}), 200
    else:
        return jsonify({'message': 'Method not supported'}), 500


@app.route('/positions/<position_id>', methods=['GET'])
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
            company_id = request.args['company_id']
            result = web_ctrl.get_positions(company_id=company_id)
        return JSONEncoder().encode(result)
    else:
        return {"error": "method {} not supported!".format(request.method)}


@app.route('/engagements', methods=['POST', 'GET', 'PUT'])
def engagements():
    result = ""
    if request.method == 'POST':
        engagement = request.get_json()
        web_ctrl = WebController.getInstance()
        result = {"engagement_id": str(web_ctrl.add_engagement(engagement))}
        return jsonify(result)
    if request.method == 'PUT':
        engagement = request.get_json()
        web_ctrl = WebController.getInstance()
        result = {"engagement_id": str(web_ctrl.modify_engagement(engagement))}
        return jsonify(result)
    elif request.method == 'GET':
        web_ctrl = WebController.getInstance()
        try:
            position_id = request.args['position_id']
            result = web_ctrl.get_engagements(position_id=position_id)
        except exceptions.BadRequestKeyError:
            try:
                engagement_id = request.args['engagement_id']
                result = web_ctrl.get_engagements(engagement_id=engagement_id)
            except exceptions.BadRequestKeyError:
                print("no engagement args")
        return JSONEncoder().encode(result)
    else:
        return {"error": "method {} not supported!".format(request.method)}


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    try:
        engagement_id = request.args['engagement_id']
        if request.method == 'POST':
            feedback_text = request.get_json()['feedback_text']
            web_ctrl = WebController.getInstance()
            result = {"feedback_id": str(web_ctrl.post_feedback(feedback_text, engagement_id))}
            return jsonify(result)
        elif request.method == 'GET':
            web_ctrl = WebController.getInstance()
            result = web_ctrl.get_feedback(engagement_id=engagement_id)
            return JSONEncoder().encode(result)
        else:
            return {"error": "method {} not supported!".format(request.method)}
    except exceptions.BadRequestKeyError:
        return {"error": "missing mandatory argument engagement_id"}


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


@app.route('/resources/cities')
def cities():
    res_control = ResourcesController.get_instance()
    if request.method == 'GET':
        result = res_control.get_all_cities()

    return JSONEncoder().encode(result)


@app.route('/student/getStudentEngagements/<student_id>', methods=['GET'])
@app.route('/student/getStudentEngagements', methods=['POST', 'GET'])
@jwt_required
def get_student_engagements(student_id=None):
    result = None
    if request.method == 'POST':
        request_data = request.get_json()
        student_id = request_data['student_id']
        limit = request_data['limit']
        result = MobileController.get_student_engagements2(student_id=student_id, limit=limit)
    elif request.method == 'GET':
        result = MobileController.get_student_engagements2(student_id=student_id)
    return JSONEncoder().encode(result)


@app.route('/resources/getPositionDataSet', methods=['GET'])
def get_position_dataset():
    result = None
    if request.method == 'GET':
        result = MobileController.get_position_dataset()
    return JSONEncoder().encode(result)


@app.route('/student/engagement_update', methods=['POST'])
@jwt_required
def get_student_engagement_update():
    if request.method == 'POST':
        request_data = request.get_json()
        student_id = request_data['student_id']
        engagement_id = request_data['engagement_id']
        update_fields = request_data['update_fields']
        result = MobileController.get_student_engagement_update(student_id=student_id, engagement_id=engagement_id,
                                                                update_fields=update_fields)
    return JSONEncoder().encode(result)


@app.route('/student/wish_list_save', methods=['POST'])
@jwt_required
def set_wish_list_save():
    if request.method == 'POST':
        request_data = request.get_json()
        student_id = request_data['student_id']
        wish_list = request_data['wish_list']

        result = MobileController.wish_list_save(student_id=student_id, wish_list=wish_list)
    return JSONEncoder().encode(result)


@app.route('/student/wish_list/calculate_suggested_skill', methods=['POST'])
@jwt_required
def calculate_suggested_skill():
    if request.method == 'POST':
        request_data = request.get_json()
        student_id = request_data['student_id']
        student_skills = request_data['student_skills']
        wl_positions = request_data['wl_positions']
        result = Match.wl_suggestion_skill_id(student_id=student_id, student_skills=student_skills,
                                              wl_positions=wl_positions)
    return JSONEncoder().encode(result)


@app.route('/student/get_wish_list', methods=['POST'])
@jwt_required
def get_wish_list():
    if request.method == 'POST':
        request_data = request.get_json()
        student_id = request_data['student_id']

        result = MobileController.get_wish_list(student_id=student_id)
    return JSONEncoder().encode(result)


@app.route('/student/get_student_engagement_by_match', methods=['POST', 'GET'])
@jwt_required
def get_student_engagement_by_match():
    result = None
    if request.method == 'POST':
        request_data = request.get_json()
        student_id = request_data['student_id']
        match_id = request_data['match_id']
        # result = MobileController.get_student_engagement_by_match(student_id=student_id,match_id=match_id)
        result = MobileController.get_student_engagement_by_match2(match_id=match_id)
    elif request.method == 'GET':
        pass
    return JSONEncoder().encode(result[0])


@app.route('/student/skills/<student_id>', methods=['POST', 'GET'])
@jwt_required
def get_student_skills(student_id):
    result = None
    if request.method == 'POST':
        result = MobileController.get_student_skills(student_id)
    if request.method == 'GET':
        result = MobileController.get_student_skills(student_id)

    return JSONEncoder().encode(result)


@app.route('/position/skills/<position_id>', methods=['POST', 'GET'])
@jwt_required
def get_position_skills(position_id):
    result = None
    if request.method == 'POST':
        result = MobileController.get_position_skills(position_id=position_id)
    if request.method == 'GET':
        result = MobileController.get_position_skills(position_id=position_id)

    return JSONEncoder().encode(result)


@app.route('/student/update_skills/<student_id>', methods=['POST', 'GET'])
@jwt_required
def set_student_skills(student_id):
    skills = request.get_json()
    if request.method == 'POST':
        mob_ctrl = MobileController()
        result = mob_ctrl.set_student_skills(student_id, skills)
    if request.method == 'GET':
        mob_ctrl = MobileController()
        result = mob_ctrl.set_student_skills(student_id, skills)

    return JSONEncoder().encode(result)


@app.route('/matches', methods=['GET'])
def matches():
    if request.method == 'GET':
        web_ctrl = WebController.getInstance()
        try:
            position_id = request.args['position_id']
            result = web_ctrl.get_matches(position_id=position_id)
        except exceptions.BadRequestKeyError:
            try:
                student_id = request.args['student_id']
                result = web_ctrl.get_matches(student_id=student_id)
            except exceptions.BadRequestKeyError:
                result = web_ctrl.get_matches()
        return JSONEncoder().encode(result)
    else:
        return {"error": "method {} not supported!".format(request.method)}


# Boot functions

def get_companies_list():
    web_ctrl = WebController.getInstance()
    return web_ctrl.get_companies_list()


if __name__ == '__main__':
    if config.read_app_settings(Key='ServerDebug') == '1':
        app.debug = True
    if config.read_app_settings(Key='RunMatchEngine') == '1':
        example = JobThread(interval=Utils.int_try_parse(config.read_job(Key='DELAY_INTERVAL'), 20))

    companies = get_companies_list()
    app.run(port=5050, threaded=True)
