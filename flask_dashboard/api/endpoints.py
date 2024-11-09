from flask import Blueprint, jsonify
import pandas as pd

api_blueprint = Blueprint('api', __name__)

# Sample data
data = pd.DataFrame({"date": ["2023-01-01", "2023-01-02"], "price": [70, 72]})

@api_blueprint.route('/data', methods=['GET'])
def get_data():
    """Endpoint to get historical data."""
    return jsonify(data.to_dict(orient="records"))

@api_blueprint.route('/metrics', methods=['GET'])
def get_metrics():
    """Endpoint to get model performance metrics."""
    metrics = {"RMSE": 1.2, "MAE": 1.0}  # Dummy data
    return jsonify(metrics)
