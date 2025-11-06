# 🌿 Plant Disease Detection using CNN + PSO Optimization

This project is a **full-stack deep learning web app** that detects plant leaf diseases using **Convolutional Neural Networks (CNN)** and a **Particle Swarm Optimization (PSO)-tuned CNN** model.  

Users can upload a leaf image, and the app will display predictions from both models for comparison.

---
 <img src="assets/extension_screenshot.png" alt="Extension Screenshot" width="1000">
## 🚀 Live Demo

### 🌐 Frontend (Netlify)
👉 [Plant Disease Detection - Live Website](https://coruscating-scone-6c051c.netlify.app)

### ⚙️ Backend (Render)
👉 [Backend API Endpoint](https://cnn-pso-plant-disease-prediction.onrender.com)

---

## 🧩 Features

- 🌱 Upload plant leaf images directly from browser
- 🤖 Compare predictions from **baseline CNN** and **PSO-optimized CNN**
- 📊 Real-time confidence scores
- ☁️ Hosted using **Render (backend)** and **Netlify (frontend)**
- 🔐 CORS-enabled and mobile responsive

---

## 🏗️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Flask (Python) |
| **Machine Learning** | TensorFlow / Keras |
| **Deployment** | Render (API) + Netlify (Frontend) |
| **Optimization** | Particle Swarm Optimization (PSO) |

---

## 🧠 How It Works

1. The user uploads a leaf image from the frontend.
2. The frontend sends it to the Flask API (`/predict` endpoint).
3. The backend:
   - Preprocesses the image
   - Runs inference using both CNN models
   - Returns predicted class + confidence score
4. The frontend displays the predictions neatly.

---



