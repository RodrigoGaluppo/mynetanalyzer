from flask import Flask
from flask_cors import CORS
from controllers.Host import host_blueprint
from controllers.User import user_blueprint
from Global import initialize_default_user

app = Flask(__name__)
CORS(app)

app.register_blueprint(host_blueprint, url_prefix='/hosts')
app.register_blueprint(user_blueprint, url_prefix='/users')

initialize_default_user()

if __name__ == '__main__':
    print("manager alive")
    app.run(debug=True, port=5001)
