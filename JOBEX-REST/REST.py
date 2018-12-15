
from flask import Flask,jsonify,request
from DAL import MobileDbHandler

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

@app.route('/Status')
def getConnectionStatus():
    mobiledb = MobileDbHandler.MobileDbHandler.getInstance()
    return  mobiledb.status()

if __name__ == '__main__':
    app.run(port=5050)
