# -*- coding: utf-8 -*-
"""App.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NVXkiBtTPJJ4yIJur7lEwWikWSuj5akd
"""

import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import nltk

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load the pre-trained model
model = load_model("sentiment_model.h5")

# Load tokenizer (recreate the tokenizer used during training)
import pickle
with open("tokenizer.pkl", "rb") as file:
    tokenizer = pickle.load(file)

# Preprocessing functions
stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]  # Remove stopwords
    words = [lemmatizer.lemmatize(word) for word in words]  # Lemmatize
    return ' '.join(words)

def predict_sentiment(text):
    processed_text = preprocess_text(text)
    sequence = tokenizer.texts_to_sequences([processed_text])
    padded_sequence = pad_sequences(sequence, maxlen=100, padding='post')
    prediction = model.predict(padded_sequence)
    return prediction[0][0]

# Streamlit UI
st.title("Sentiment Analysis")
st.write("Enter a review below to predict whether it's positive or negative.")

# Input text from user
user_input = st.text_area("Enter your review:")

if st.button("Analyze"):
    if user_input.strip():
        prediction = predict_sentiment(user_input)
        if prediction >= 0.5:
            st.success(f"Positive sentiment with a confidence of {prediction:.2f}")
        else:
            st.error(f"Negative sentiment with a confidence of {1 - prediction:.2f}")
    else:
        st.warning("Please enter some text to analyze!")