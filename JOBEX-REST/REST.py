from flask import Flask,jsonify,request
from Controllers import MobileController,WebController

app = Flask(__name__)



#1st push
@app.route('/')
def home():
    pass

@app.route('/user')
def create_user():
    jsonStr = {"user":"nie","skills":[{"id":1,"skillName":"Hi Nir"},{"id":1,"skillName":"Hi Nir"}]}
    return jsonify(jsonStr)

@app.route('/login')
def get_restaurants():
    jsonStr = {"user": "nie", "skills": [{"id": 1, "skillName": "Hi Nir"}, {"id": 1, "skillName": "Hi Nir"}]}
    return jsonify(jsonStr)\

@app.route('/StatusMob')
def getMobStatus():
    mobCtrl = MobileController.MobileController.getInstance()
    return  mobCtrl.status()

@app.route('/StatusWeb')
def getWebStatus():
    webCtrl = WebController.WebController.getInstance()
    return webCtrl.status()

if __name__ == '__main__':
    app.run(port=5050)
