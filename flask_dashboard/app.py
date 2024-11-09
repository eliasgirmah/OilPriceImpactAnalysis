from flask import Flask
from flask_cors import CORS
from api.endpoints import api_blueprint  # Ensure this import is correct

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Register the API blueprint with the '/api' prefix
app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
