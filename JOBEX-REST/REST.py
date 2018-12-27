from flask import Flask, jsonify, request
from flask_cors import CORS
from mobile_controller import MobileController
from web_controller import WebController
from auth_controller import AuthController
from Utils import config_helper

app = Flask(__name__)
CORS(app)
config = config_helper.ConfigHelper()


# 1st push
@app.route('/')
def home():
    json_str = {"result": 0}
    return jsonify(json_str)


@app.route('/user', methods=['POST', 'GET'])
def create_user():
    if request.method == 'POST':
        json_str = {"result": 0}
        return json_str
    elif request.method == 'GET':
        json_str = {"user": "nie", "skills": [{"id": 1, "skillName": "Hi Nir"}, {"id": 1, "skillName": "Hi Nir"}]}
        return jsonify(json_str)


@app.route('/login', methods=['POST', 'GET'])
def get_login():
    if request.method == 'POST':
        authentication = request.get_json()
        username = authentication['username']
        password = authentication['password']

        auth_ctrl = AuthController.get_instance()
        result = auth_ctrl.login(username, password)
        return jsonify(str(result))
    elif request.method == 'GET':
        authentication = request.get_json()
        username = authentication['username']
        password = authentication['password']
        auth_ctrl = AuthController.get_instance()
        result = auth_ctrl.login(username, password)
        return jsonify(str(result))


@app.route('/checkAuthenticationStatus', methods=['POST'])
def get_authentication_status():
    if request.method == 'POST':
        authentication = request.get_json()
        sentUId = authentication['user_id']
        token = authentication['authToken']
        decriptecdUId = AuthController.decode_auth_token(token)
        result = {"sentUId": sentUId , "decriptecdUId":decriptecdUId}
        return jsonify(result)


@app.route('/getStudentEngagements/<student_Id>')
def get_student_engagements(student_id):
    mob_ctrl = MobileController.get_instance()
    result = mob_ctrl.get_StudentEngagements(studentId=student_id)
    return result


@app.route('/WebLogin')
def web_login():
    return 'Web Login'


@app.route('/MobileLogin')
def mob_login():
    return 'Mobile Login'


@app.route('/StatusMob')
def get_mob_status():
    mob_ctrl = MobileController.get_instance()
    return mob_ctrl.status()


@app.route('/StatusWeb')
def get_web_status():
    web_ctrl = WebController.get_instance()
    return web_ctrl.status()


@app.route('/register/new_student', methods=['POST', 'GET'])
def register_student():
    if request.method == 'POST':
        student = request.get_json()
        mob_ctrl = MobileController.get_instance()
        result = {
            "student_user_id" : str(mob_ctrl.register_student(student))
        }
        return jsonify(result)
    else:
        user = request.args.get_json()
        return jsonify(user)


@app.route('/create_employee', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.values

        return jsonify(user)
    else:
        user = request.args.get_json()
        return jsonify(user)


if __name__ == '__main__':
    if config.read_app_settings(Key='ServerDebug') == '1':
        app.debug = True
    app.run(port=5050)
