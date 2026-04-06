import os
import tensorflow as tf
import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "plant_model (1).keras")
model = tf.keras.models.load_model(MODEL_PATH, compile=False)

# Load model safely
try:
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
except Exception as e:
    print("❌ Error loading model:", e)
    model = None


class_names = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'Blueberry___healthy', 
               'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
               'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)',
                 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 
                 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy',
                   'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight',
                     'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 
                     'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']

# Mapping technical names to proper readable names
PROPER_NAMES = {
    'Apple___Apple_scab': 'Apple Scab',
    'Apple___Black_rot': 'Apple Black Rot',
    'Apple___Cedar_apple_rust': 'Apple Cedar Rust',
    'Apple___healthy': 'Apple (Healthy)',
    'Blueberry___healthy': 'Blueberry (Healthy)',
    'Cherry_(including_sour)___Powdery_mildew': 'Cherry Powdery Mildew',
    'Cherry_(including_sour)___healthy': 'Cherry (Healthy)',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 'Corn Gray Leaf Spot',
    'Corn_(maize)___Common_rust_': 'Corn Common Rust',
    'Corn_(maize)___Northern_Leaf_Blight': 'Corn Northern Leaf Blight',
    'Corn_(maize)___healthy': 'Corn (Healthy)',
    'Grape___Black_rot': 'Grape Black Rot',
    'Grape___Esca_(Black_Measles)': 'Grape Esca (Black Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 'Grape Leaf Blight',
    'Grape___healthy': 'Grape (Healthy)',
    'Orange___Haunglongbing_(Citrus_greening)': 'Citrus Greening (HLB)',
    'Peach___Bacterial_spot': 'Peach Bacterial Spot',
    'Peach___healthy': 'Peach (Healthy)',
    'Pepper,_bell___Bacterial_spot': 'Bell Pepper Bacterial Spot',
    'Pepper,_bell___healthy': 'Bell Pepper (Healthy)',
    'Potato___Early_blight': 'Potato Early Blight',
    'Potato___Late_blight': 'Potato Late Blight',
    'Potato___healthy': 'Potato (Healthy)',
    'Raspberry___healthy': 'Raspberry (Healthy)',
    'Soybean___healthy': 'Soybean (Healthy)',
    'Squash___Powdery_mildew': 'Squash Powdery Mildew',
    'Strawberry___Leaf_scorch': 'Strawberry Leaf Scorch',
    'Strawberry___healthy': 'Strawberry (Healthy)',
    'Tomato___Bacterial_spot': 'Tomato Bacterial Spot',
    'Tomato___Early_blight': 'Tomato Early Blight',
    'Tomato___Late_blight': 'Tomato Late Blight',
    'Tomato___Leaf_Mold': 'Tomato Leaf Mold',
    'Tomato___Septoria_leaf_spot': 'Tomato Septoria Leaf Spot',
    'Tomato___Spider_mites Two-spotted_spider_mite': 'Tomato Spider Mites',
    'Tomato___Target_Spot': 'Tomato Target Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'Tomato Yellow Leaf Curl Virus',
    'Tomato___Tomato_mosaic_virus': 'Tomato Mosaic Virus',
    'Tomato___healthy': 'Tomato (Healthy)'
}


DISEASE_REMEDIES = {
    # Apple
    'Apple Scab': 'Apply fungicides like Captan or Sulfur. Rake and destroy fallen leaves to prevent overwintering.',
    'Apple Black Rot': 'Prune out dead wood and remove "mummified" fruit. Apply fungicides during the early season.',
    'Apple Cedar Rust': 'Remove nearby Eastern Red Cedar trees if possible. Use Myclobutanil fungicides at pink bud stage.',
    'Apple (Healthy)': 'No treatment needed. Maintain proper pruning and thinning.',
    
    # Corn
    'Corn Gray Leaf Spot': 'Use resistant hybrids and practice crop rotation. Apply foliar fungicides if infection is severe.',
    'Corn Common Rust': 'Plant resistant varieties. Most infections do not require fungicides unless they appear very early.',
    'Corn Northern Leaf Blight': 'Rotate crops with non-grass species. Use fungicides like Azoxystrobin if detected before silking.',
    'Corn (Healthy)': 'Monitor for pests. Maintain optimal nitrogen levels.',
    
    # Grapes
    'Grape Black Rot': 'Ensure good air circulation via pruning. Use Mancozeb or Myclobutanil fungicides early in the season.',
    'Grape Esca (Black Measles)': 'Protect pruning wounds with sealants. Remove and burn heavily infected vines.',
    'Grape Leaf Blight': 'Remove infected leaves. Apply copper-based fungicides if humidity is high.',
    'Grape (Healthy)': 'Continue standard irrigation and fertilization schedule.',
    
    # Potato & Tomato (Blights)
    'Potato Early Blight': 'Apply Chlorothalonil or Copper fungicides. Rotate crops every 2-3 years.',
    'Potato Late Blight': 'Remove infected plants immediately. Use systemic fungicides and avoid overhead irrigation.',
    'Tomato Early Blight': 'Prune lower leaves to prevent soil splash. Use Copper sprays or Neem oil.',
    'Tomato Late Blight': 'Highly contagious. Remove and destroy infected plants. Use preventive fungicides in wet weather.',
    'Tomato Septoria Leaf Spot': 'Avoid overhead watering. Apply fungicides containing Chlorothalonil or Mancozeb.',
    
    # Viruses (No Cure)
    'Citrus Greening (HLB)': 'No known cure. Remove infected trees to prevent spread. Control the Asian Citrus Psyllid vector.',
    'Tomato Yellow Leaf Curl Virus': 'No cure. Control Whitefly populations using Neem oil or sticky traps. Remove infected plants.',
    'Tomato Mosaic Virus': 'No cure. Remove and burn infected plants. Wash hands and tools after handling infected vines.',
    
    # Others
    'Squash Powdery Mildew': 'Improve air circulation. Apply Sulfur-based fungicides or a milk-water spray (40/60 ratio).',
    'Tomato Spider Mites': 'Spray plants with a strong stream of water to dislodge mites. Use Insecticidal soap or Neem oil.',
    'Strawberry Leaf Scorch': 'Remove old infected leaves. Avoid high-nitrogen fertilizers which promote soft, susceptible growth.',
    
    # General Healthy
    'Healthy': 'Plant is healthy! Maintain regular scouting and balanced nutrition.'
}

def predict_disease(image_path):
    if model is None:
        return "Model not loaded", 0.0

    img = Image.open(image_path).convert("RGB").resize((128, 128))  # match training size
    img_array = np.array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    idx = int(np.argmax(prediction))

    raw_class = class_names[idx]

    proper_name = PROPER_NAMES.get(raw_class,raw_class)

    remedy = DISEASE_REMEDIES.get(proper_name, "Consult a local agricultural expert for treatment.")
    confidence = float(np.max(prediction)) * 100

    return proper_name, round(confidence, 2),remedy

