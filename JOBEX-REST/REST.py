from flask import Flask, jsonify, request, redirect, url_for

import config_helper
from mobile_controller import MobileController
from web_controller import WebController


app = Flask(__name__)

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


@app.route('/login/<type>')
def get_loginSoruce(type):
    if type == 'Web' or type == 'web':
        return redirect(url_for('web_login'))
    elif type == 'Mobile' or type == 'mobile':
        return redirect(url_for('mob_login'))


@app.route('/getStudentEngagements/<StudentId>')
def get_StudentEngagements(StudentId):
    mobCtrl = MobileController.getInstance()
    result = mobCtrl.get_StudentEngagements(studentId=StudentId)
    return result


@app.route('/WebLogin')
def web_login():
    return 'Web Login'


@app.route('/MobilebLogin')
def mob_login():
    return 'Mobile Login'


@app.route('/StatusMob')
def getMobStatus():
    mobCtrl = MobileController.MobileController.getInstance()
    return mobCtrl.status()


@app.route('/StatusWeb')
def getWebStatus():
    webCtrl = WebController.WebController.getInstance()
    return webCtrl.status()


if __name__ == '__main__':
    if config.readAppSettings(Key='ServerDebug') == '1':
        app.debug = True
        app.run(port=5050)
    else:
        app.run(port=5050)
