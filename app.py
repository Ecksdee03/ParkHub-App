from flask import Flask, session
from views import views
# Run pip install python-dotenv first
from dotenv import load_dotenv
from datetime import timedelta
from flask_cors import CORS
import secrets
load_dotenv()  # This loads variables from .env into the environment

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(views, url_prefix = "/views")

# Secret key is necessary for session management
app.secret_key = secrets.token_hex(16)

app.permanent_session_lifetime = timedelta(days=30)

if __name__ == "__main__":
    app.run(debug=True, port=8000)



