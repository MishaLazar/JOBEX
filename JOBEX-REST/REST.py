from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_cors import CORS
from mobile_controller import MobileController
from web_controller import WebController
from Controllers.auth_controller import AuthController
from Utils import config_helper

app = Flask(__name__)
CORS(app)
config = config_helper.ConfigHelper.get_instance()
app.config['JWT_SECRET_KEY'] = config.read_auth('SECRET_KEY')
jwt = JWTManager(app)


@app.route('/')
def home():
    json_str = {"result": 0}
    return jsonify(json_str)


@app.route('/login', methods=['POST', 'GET'])
def get_login():
    if request.method == 'POST':
        authentication = request.get_json()
        username = authentication['username']
        password = authentication['password']

        result = AuthController.login(username, password)
        if result:
            access_token = create_access_token(identity=result['user_id'])
            refresh_token = create_refresh_token(identity=result['user_id'])
            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token
                }), 200
        else:
            return jsonify({'message': 'Wrong credentials'}), 403


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


@app.route('/getStudentEngagements/<student_Id>')
def get_student_engagements(student_id):
    mob_ctrl = MobileController.get_instance()
    result = mob_ctrl.get_StudentEngagements(studentId=student_id)
    return result


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


if __name__ == '__main__':
    if config.read_app_settings(Key='ServerDebug') == '1':
        app.debug = True
    app.run(port=5050)
