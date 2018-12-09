from flask import Flask,jsonify,request

app = Flask(__name__)



#1st push
@app.route('/')
def home():
    pass

@app.route('/user')
def create_user():
    jsonStr = {"user":"nie","skills":[{"id":1,"skillName":"Hi Nir"},{"id":1,"skillName":"Hi Nir"}]}
    return jsonify(jsonStr)


if __name__ == '__main__':
    app.run(port=5000)
