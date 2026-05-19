from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import pickle
import numpy as np
import os

app = Flask(__name__)

# Pre-load model and tokenizer
print("Loading model and tokenizer...")
model = None
tokenizer = None
max_len = None  # <-- Ensure max_len is globally available

def load_model_and_tokenizer():
    global model, tokenizer, max_len  # <-- Declare max_len as global
    try:
        # Load the model
        model = tf.keras.models.load_model('model/model.keras')
        
        # Load the tokenizer and max_len
        with open('model/tokenizer.pkl', 'rb') as tokenizer_file:
            tokenizer_data = pickle.load(tokenizer_file)

        tokenizer = tokenizer_data["tokenizer"]
        max_len = tokenizer_data["max_len"]  # <-- Assign to global variable

        print("Model and tokenizer loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading model or tokenizer: {e}")
        return False

# Load model at startup
load_model_and_tokenizer()

def preprocess_text(text):
    if tokenizer is None or max_len is None:
        raise ValueError("Tokenizer or max_len not loaded properly.")
    
    sequences = tokenizer.texts_to_sequences([text])
    padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(
        sequences, maxlen=max_len, padding='post'
    )
    return padded_sequence

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or tokenizer is None:
        return jsonify({'error': 'Model or tokenizer not loaded'}), 500
    
    # Get the text from the request
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        # Preprocess the text
        processed_text = preprocess_text(text)
        
        # Make prediction
        prediction = model.predict(processed_text)
        
        # Get the prediction result
        is_spam = bool(prediction[0][0] > 0.5)
        confidence = float(prediction[0][0]) if is_spam else float(1 - prediction[0][0])
        
        return jsonify({
            'is_spam': is_spam,
            'confidence': confidence,
            'text': text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
