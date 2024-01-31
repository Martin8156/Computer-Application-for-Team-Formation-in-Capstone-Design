from flask import Flask

api = Flask(__name__)

@api.route('/profile')
def my_profile():
    response_body = {
        "name": "Nagato",
        "about" :"Gabriel Mount, Ethan Nguyen, Nathan Stodola"
    }

    return response_body