import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import joblib
import numpy as np

# ---------------------------------------------------
# INITIALIZE FLASK APP
# ---------------------------------------------------
app = Flask(__name__)
CORS(app)

# ---------------------------------------------------
# MODEL PATHS
# ---------------------------------------------------
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
CROP_MODEL_PATH = os.path.join(MODEL_DIR, "crop_model.pkl")
CROP_ENCODER_PATH = os.path.join(MODEL_DIR, "crop_encoder.pkl")
MODEL_FEATURES_PATH = os.path.join(MODEL_DIR, "model_features.pkl")
FERTILIZER_RATIOS_PATH = os.path.join(MODEL_DIR, "fertilizer_ratios.pkl")

# ---------------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------------
CROP_MODEL = None
CROP_ENCODER = None
MODEL_FEATURES = []
FERTILIZER_RATIOS = {}

# ---------------------------------------------------
# LOAD MODELS
# ---------------------------------------------------
def load_models():
    global CROP_MODEL, CROP_ENCODER, MODEL_FEATURES, FERTILIZER_RATIOS

    try:
        CROP_MODEL = joblib.load(CROP_MODEL_PATH)
        print("Crop Model loaded successfully.")

        CROP_ENCODER = joblib.load(CROP_ENCODER_PATH)
        print("Crop Encoder loaded successfully.")

        MODEL_FEATURES = joblib.load(MODEL_FEATURES_PATH)
        print(f"Model Features loaded: {len(MODEL_FEATURES)} features.")

        FERTILIZER_RATIOS = joblib.load(FERTILIZER_RATIOS_PATH)
        print("Fertilizer Ratios loaded successfully.")

    except Exception as e:
        print(f"Error loading models: {e}")

load_models()

# ---------------------------------------------------
# ROUTES
# ---------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return "Agri-Tech ML API is running on localhost!", 200

@app.route("/predict", methods=["POST"])
def predict_crop():
    if not CROP_MODEL:
        return jsonify({"recommended_crop": None, "error": "Model not loaded"}), 500

    try:
        data = request.get_json()

        # Numeric features
        required_numeric = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
        input_data = {}
        for feature in required_numeric:
            if feature not in data:
                return jsonify({"error": f"Missing {feature}"}), 400
            input_data[feature] = float(data[feature])

        # Soil type as number (instead of one-hot)
        soil_type = data.get("soil_type")
        if soil_type is None:
            return jsonify({"error": "Missing soil_type"}), 400

        # Map soil type string to numeric value
        soil_mapping = {"Alluvial": 0, "Loamy": 1, "Loamy (Light Soil)": 2, 
                        "Sandy Loam": 3, "Black Soil (Regur)": 4, "Laterite": 5}
        soil_num = soil_mapping.get(soil_type)
        if soil_num is None:
            return jsonify({"error": f"Soil type '{soil_type}' not recognized"}), 400

        # Prepare feature vector in correct order (8 features)
        final_features = np.array([
            input_data["N"], input_data["P"], input_data["K"],
            input_data["temperature"], input_data["humidity"], input_data["ph"],
            input_data["rainfall"], soil_num
        ]).reshape(1, -1)

        # Prediction
        pred_encoded = CROP_MODEL.predict(final_features)[0]

        # If your model uses LabelEncoder to encode crop names
        if CROP_ENCODER:
            pred_label = CROP_ENCODER.inverse_transform([pred_encoded])[0]
        else:
            pred_label = str(pred_encoded)

        return jsonify({"recommended_crop": pred_label, "error": None})

    except Exception as e:
        print("Prediction Error:", e)
        return jsonify({"error": str(e)}), 500



'''@app.route("/predict", methods=["POST"])
def predict_crop():
    if not CROP_MODEL or not CROP_ENCODER or not MODEL_FEATURES:
        return jsonify({"recommended_crop": None, "error": "Model not loaded"}), 500

    try:
        data = request.get_json()

        required_numeric = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

        # Validate numeric features
        input_data = {}
        for feature in required_numeric:
            if feature not in data:
                return jsonify({"error": f"Missing {feature}"}), 400
            input_data[feature] = float(data[feature])

        # Validate soil type
        soil_type = data.get("soil_type")
        if not soil_type:
            return jsonify({"error": "Missing soil_type"}), 400

        # Prepare final feature vector
        final_dict = {}

        # Add numeric features
        for f in required_numeric:
            final_dict[f] = input_data[f]

        # Initialize all one-hot soil features as 0
        ohe_cols = [col for col in MODEL_FEATURES if col.startswith("soil_type_")]
        for col in ohe_cols:
            final_dict[col] = 0

        soil_ohe = f"soil_type_{soil_type}"
        if soil_ohe not in final_dict:
            return jsonify({"error": f"Soil type '{soil_type}' not recognized"}), 400

        final_dict[soil_ohe] = 1

        # Create final feature vector in correct order
        final_features = np.array([final_dict[f] for f in MODEL_FEATURES]).reshape(1, -1)

        # Prediction
        pred_encoded = CROP_MODEL.predict(final_features)[0]
        pred_label = CROP_ENCODER.inverse_transform([pred_encoded])[0]

        return jsonify({"recommended_crop": pred_label, "error": None})

    except Exception as e:
        print("Prediction Error:", e)
        return jsonify({"error": str(e)}), 500

'''
@app.route("/fertilizer_recommendation", methods=["POST"])
def fertilizer_recommendation():
    try:
        data = request.get_json()
        crop = data.get("crop", "").lower()

        if not crop:
            return jsonify({"error": "Missing crop name"}), 400

        if crop not in FERTILIZER_RATIOS:
            return jsonify({"error": f"No fertilizer data for crop '{crop}'"}), 404

        ratio = FERTILIZER_RATIOS[crop]

        return jsonify({
            "recommended_ratio": {
                "N": ratio.get("N"),
                "P": ratio.get("P"),
                "K": ratio.get("K")
            },
            "error": None
        })

    except Exception as e:
        print("Fertilizer Error:", e)
        return jsonify({"error": str(e)}), 500

# ---------------------------
# TEST MODEL LOADING
# ---------------------------
def test_models():
    try:
        crop_model = joblib.load(CROP_MODEL_PATH)
        crop_encoder = joblib.load(CROP_ENCODER_PATH)
        model_features = joblib.load(MODEL_FEATURES_PATH)
        fertilizer_ratios = joblib.load(FERTILIZER_RATIOS_PATH)
        print("✅ All models loaded successfully!")
        print(f" - Crop model type: {type(crop_model)}")
        print(f" - Crop encoder type: {type(crop_encoder)}")
        print(f" - Number of features: {len(model_features)}")
        print(f" - Fertilizer ratios loaded for {len(fertilizer_ratios)} crops")
    except Exception as e:
        print("❌ Error loading models:", e)

# ---------------------------------------------------
# RUN LOCALHOST SERVER
# ---------------------------------------------------

if __name__ == "__main__":
    test_models()  # Test if all models load correctly
    print("Starting Flask server on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=True)

