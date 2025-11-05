from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io, gc, tensorflow as tf

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# -------- Lazy Model Load --------
baseline_model = None
pso_model = None

def load_models():
    global baseline_model, pso_model
    if baseline_model is None:
        baseline_model = load_model("models/cnn_baseline.h5")
    if pso_model is None:
        pso_model = load_model("models/cnn_pso_tuned.h5")


# -------- Class Names --------
CLASSES = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
    "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy"
]

IMG_SIZE = (128, 128)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    return response

def preprocess(image_file):
    img = Image.open(io.BytesIO(image_file.read())).convert("RGB")
    img = img.resize(IMG_SIZE)
    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    global baseline_model, pso_model

    if request.method == "OPTIONS":
        res = jsonify({"message": "CORS OK"})
        res.headers.add("Access-Control-Allow-Origin", "*")
        res.headers.add("Access-Control-Allow-Headers", "Content-Type")
        res.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return res, 200

    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
        
        load_models()
        img = preprocess(request.files["image"])

        base_prob = baseline_model.predict(img, verbose=0)[0]
        pso_prob = pso_model.predict(img, verbose=0)[0]

        base_idx = np.argmax(base_prob)
        pso_idx = np.argmax(pso_prob)

        response = jsonify({
            "baseline_prediction": CLASSES[base_idx],
            "baseline_confidence": float(base_prob[base_idx]),
            "pso_prediction": CLASSES[pso_idx],
            "pso_confidence": float(pso_prob[pso_idx])
        })

        # ✅ Free memory so Render doesn't crash
        tf.keras.backend.clear_session()
        gc.collect()
        baseline_model = None
        pso_model = None

        return response

    except Exception as e:
        print("Backend Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend running"})
