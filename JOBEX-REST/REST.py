from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS , cross_origin

import config_helper
from mobile_controller import MobileController
from web_controller import WebController

app = Flask(__name__)
CORS(app)
config = config_helper.ConfigHelper()


# 1st push
@app.route('/')
def home():
    json_str = {"result": 0}
    return jsonify(json_str)


@app.route('/user')
def create_user():
    json_str = {"user": "nie", "skills": [{"id": 1, "skillName": "Hi Nir"}, {"id": 1, "skillName": "Hi Nir"}]}
    return jsonify(json_str)


@app.route('/login/<login_type>')
def get_login_source(login_type):
    if login_type == 'Web' or login_type == 'web':
        return redirect(url_for('web_login'))
    elif login_type == 'Mobile' or login_type == 'mobile':
        return redirect(url_for('mob_login'))


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
    if config.readAppSettings(Key='ServerDebug') == '1':
        app.debug = True
        app.run(port=5050)
    else:
        app.run(port=5050)
