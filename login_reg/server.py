from flask_app import app
from flask_app.controllers import control_users, control_messages

if __name__=="__main__":
    app.run(debug=True)