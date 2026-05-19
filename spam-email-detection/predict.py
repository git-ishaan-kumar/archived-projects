import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle

# Load model
model = tf.keras.models.load_model("model/model.keras")

# Load tokenizer and preprocessing parameters
with open("model/tokenizer.pkl", "rb") as handle:
    tokenizer_data = pickle.load(handle)

tokenizer = tokenizer_data["tokenizer"]
max_len = tokenizer_data["max_len"]

# Define the email to classify
email = input("Email: ")

# Preprocess the input email
sequence = tokenizer.texts_to_sequences([email])
padded_sequence = pad_sequences(sequence, maxlen=max_len, padding='post')

# Predict
prediction = model.predict(padded_sequence)[0][0]

# Print result
print("Spam" if prediction > 0.5 else "Ham")
