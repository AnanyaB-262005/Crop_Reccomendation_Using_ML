import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import random
# Add this code near the top of flask_backend.py
@app.route('/', methods=['GET'])
def index():
    # This simple response confirms the server is live and working
    return "Agri-Tech ML API is running successfully!", 200
    
# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for the Streamlit app running on a different port
CORS(app)

# ---------------------------
# GLOBAL DATA/MODEL SETUP (Dummy for demonstration)
# ---------------------------
DATASET_PATH = "Crop_recommendation_with_soil.csv"

# Dummy NPK Ratios for Fertilizer Recommendation
FERTILIZER_RATIOS = {
    "rice": {"N": 60, "P": 40, "K": 40},
    "maize": {"N": 120, "P": 60, "K": 40},
    "chickpea": {"N": 20, "P": 60, "K": 20},
    "kidneybeans": {"N": 40, "P": 50, "K": 30},
    "pigeonpeas": {"N": 20, "P": 60, "K": 20},
    "mothbeans": {"N": 20, "P": 40, "K": 20},
    "mungbean": {"N": 20, "P": 40, "K": 20},
    "blackgram": {"N": 20, "P": 60, "K": 20},
    "lentil": {"N": 20, "P": 40, "K": 20},
    "pomegranate": {"N": 60, "P": 50, "K": 80},
    "banana": {"N": 100, "P": 30, "K": 150},
    "mango": {"N": 40, "P": 20, "K": 40},
    "grapes": {"N": 60, "P": 30, "K": 80},
    "watermelon": {"N": 60, "P": 40, "K": 80},
    "muskmelon": {"N": 60, "P": 40, "K": 80},
    "apple": {"N": 80, "P": 40, "K": 60},
    "orange": {"N": 80, "P": 40, "K": 60},
    "papaya": {"N": 80, "P": 40, "K": 60},
    "coconut": {"N": 30, "P": 10, "K": 30},
    "cotton": {"N": 80, "P": 40, "K": 40},
    "jute": {"N": 80, "P": 40, "K": 40},
    "coffee": {"N": 100, "P": 50, "K": 70}
}


# Function to load data (used here just to show readiness)
def load_data():
    if os.path.exists(DATASET_PATH):
        try:
            df = pd.read_csv(DATASET_PATH)
            # In a real app, you would load models here: e.g., crop_model = joblib.load('crop_model.pkl')
            print("Dataset loaded successfully.")
            return df
        except Exception as e:
            print(f"Error loading CSV: {e}")
    return None

df_data = load_data()

# ---------------------------
# API Endpoints
# ---------------------------

@app.route('/predict', methods=['POST'])
def predict_crop():
    """
    Endpoint for Crop Recommendation (ML Prediction)
    Inputs: N, P, K, temperature, humidity, ph, rainfall, soil_type
    Output: recommended_crop
    """
    try:
        data = request.get_json()
        
        # --- INPUT VALIDATION (Optional but recommended) ---
        required_keys = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall", "soil_type"]
        if not all(key in data for key in required_keys):
            return jsonify({"error": "Missing required input parameters"}), 400

        # --- DUMMY PREDICTION LOGIC ---
        # In a real application, you would preprocess the data and pass it to your trained model:
        # features = pd.DataFrame([data])
        # prediction = crop_model.predict(features)[0]

        # For demonstration, we use a simple rule or random choice from the loaded data
        if df_data is not None and not df_data.empty:
            # Randomly select a crop from the dataset labels
            prediction = random.choice(df_data['label'].unique().tolist())
        else:
            # Default fallback if data loading failed
            prediction = "rice" 
            
        return jsonify({
            "recommended_crop": prediction,
            "error": None
        })

    except Exception as e:
        return jsonify({"recommended_crop": None, "error": str(e)}), 500

@app.route('/fertilizer_recommendation', methods=['POST'])
def fertilizer_recommendation():
    """
    Endpoint for Fertilizer Recommendation (Lookup/Prediction)
    Inputs: crop
    Output: recommended_ratio (N, P, K)
    """
    try:
        data = request.get_json()
        crop_name = data.get('crop', '').lower()

        if not crop_name:
            return jsonify({"error": "Missing 'crop' name"}), 400
        
        # --- LOOKUP LOGIC ---
        ratio = FERTILIZER_RATIOS.get(crop_name)
        
        if ratio:
            return jsonify({
                "recommended_ratio": ratio,
                "error": None
            })
        else:
            return jsonify({"recommended_ratio": None, "error": f"No fertilizer data found for crop: {crop_name}"}), 404

    except Exception as e:
        return jsonify({"recommended_ratio": None, "error": str(e)}), 500

if __name__ == '__main__':
    # Running the Flask app on port 5000 as configured in app_streamlit_fixed.py
    print("Starting Flask API server on http://127.0.0.1:5000...")
    app.run(debug=True, port=5000, use_reloader=False)
