from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>this is the index page! method used: {}</h2>'.format(request.method)


@app.route('/dashboard/<company_name>')
def dashboard(company_name):
    return render_template("dashboard.html", company_name=company_name)


@app.route('/engagements/<engagement_name>', methods=['GET', 'POST', 'PUT'])
def engagements(engagement_name):
    return render_template("engagement.html", engagement_name=engagement_name)


@app.route('/position', methods=['GET', 'POST', 'PUT'])
def position(position_name):
    return render_template("position.html", position_name=position_name)


@app.route('/profile', methods=['GET', 'POST', 'PUT'])
def profile():
    return render_template("profile.html")


if __name__ == '__main__':
    app.run(debug=True)
