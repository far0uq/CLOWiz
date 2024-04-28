from flask import Flask, render_template, request, jsonify
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Ensure necessary NLTK downloads
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Vectorizer for CLO descriptions
vectorizer = TfidfVectorizer()

# Load CSV files
#initializing empty DataFrames for clos_df and questions_df
clos_df = pd.DataFrame(columns=["CLO", "Description"])
questions_df = pd.DataFrame(columns=["Question"])

# Text Preprocessing Function
def preprocess_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens if token.lower() not in stopwords.words("english")]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(tokens)

# Define route for processing user input and returning result
@app.route('/predict', methods=['POST'])
def predict():
    # Get data from frontend
    data = request.get_json()
    clos_description = data['closDescription']
    question = data['question']
    
    # Format data to conform with CSV format
    #starting with CLO-0
    clos_data = {'CLO': [f'CLO-{i+1}' for i in range(len(clos_descriptions))], 'Description': clos_descriptions}
    questions_data = {'Question': questions}
    
    # Convert data to DataFrames
    clos_df_temp = pd.DataFrame(clos_data)
    questions_df_temp = pd.DataFrame(questions_data)
    
    # Append new data to existing DataFrames
    global clos_df
    global questions_df
    clos_df = clos_df.append(clos_df_temp, ignore_index=True)
    questions_df = questions_df.append(questions_df_temp, ignore_index=True)
    
    # Preprocess the data
    clos_df["Processed_Description"] = clos_df["Description"].apply(preprocess_text)
    questions_df["Processed_Question"] = questions_df["Question"].apply(preprocess_text)
    
    # Vectorize the processed CLO descriptions
    tfidf_matrix = vectorizer.fit_transform(clos_df["Processed_Description"])
    
    # Vectorize the processed question using the existing TF-IDF vectorizer
    input_tfidf = vectorizer.transform(questions_df["Processed_Question"])
    
    # Calculate similarity between the input question and each CLO description
    similarity_scores = cosine_similarity(input_tfidf, tfidf_matrix)
    
    # Find the CLO with the highest similarity score
    most_relevant_index = similarity_scores.argmax(axis=1)
    most_relevant_clo = clos_df.loc[most_relevant_index, "CLO"].values[0]
    
    return jsonify({'clo': most_relevant_clo})

# Define route for serving Sort.jsx
@app.route('/Sort')
def sort():
    return render_template('Sort.jsx')

# Define route for serving Result.jsx
@app.route('/Result')
def result():
    return render_template('Result.jsx')

if __name__ == '__main__':
    app.run(debug=True, port=1800)
