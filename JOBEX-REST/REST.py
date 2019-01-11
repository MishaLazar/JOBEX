import atexit

from flask import Flask, jsonify, request, redirect, url_for
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_cors import CORS
import config_helper
from mobile_controller import MobileController
from web_controller import WebController
from resources_controller import ResourcesController
from Controllers.auth_controller import AuthController
from json_encoder import JSONEncoder
from jobs_service import JobThread

app = Flask(__name__)

config = config_helper.ConfigHelper.get_instance()
app.config['JWT_SECRET_KEY'] = config.read_auth('SECRET_KEY')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True)
jwt = JWTManager(app)


# Job_thread init

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return AuthController.check_token_in_blacklist(jti)


@app.route('/')
def home():
    json_str = {"result": 0}
    return jsonify(json_str)


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


@app.route('/login', methods=['POST', 'GET'])
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
            access_token = create_access_token(identity=result)
            refresh_token = create_refresh_token(identity=result)
            data = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            return jsonify(data), 200
        else:
            return jsonify({"message": "Wrong credentials"}), 403


@app.route('/register', methods=['POST'])
def register_student():
    if request.method == 'POST':
        user = request.get_json()
        new_user_id = MobileController.register_user(user)
        if new_user_id:
            access_token = create_access_token(identity=new_user_id['user_id'])
            refresh_token = create_refresh_token(identity=new_user_id['user_id'])
        return jsonify({
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


@app.route('/create_employee', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.values

        return jsonify(user)
    else:
        user = request.args.get_json()
        return jsonify(user)


@app.route('/positions/<company_name>/<position_id>', methods=['POST', 'GET'])
def positions(company_name=None, position_id=None):
    if request.method == 'POST':
        position = request.get_json()
        web_ctrl = WebController.getInstance()
        result = {"position_id": str(web_ctrl.add_position(position))}
        return jsonify(result)
    elif request.method == 'GET':
        web_ctrl = WebController.getInstance()
        if company_name and position_id:
            result = web_ctrl.get_positions(company_name=company_name, position_id=position_id)
        elif company_name:
            result = web_ctrl.get_positions(company_name=company_name)
        return jsonify(result)
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
        return jsonify(result)
    else:
        return {"error": "method {} not supported!".format(request.method)}


@app.route('/resources/skills' , methods=['POST', 'GET'])
def get_skills():
    if request.method == 'POST':
        result = ResourcesController.get_full_skillSet()
    elif request.method == 'GET':
        result = ResourcesController.get_full_skillSet()

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



if __name__ == '__main__':
    if config.read_app_settings(Key='ServerDebug') == '1':
        app.debug = True
    app.run(port=5050)
