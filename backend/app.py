from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Ensure necessary NLTK downloads
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Load CSV files
clos_df = pd.read_csv("clos.csv")
questions_df = pd.read_csv("questions.csv")


# Text Preprocessing Function
def preprocess_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    tokens = nltk.word_tokenize(text)
    tokens = [
        token.lower()
        for token in tokens
        if token.lower() not in stopwords.words("english")
    ]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(tokens)


# Applying Preprocessing to the DataFrames
clos_df["Processed_Description"] = clos_df["Description"].apply(preprocess_text)
questions_df["Processed_Question"] = questions_df["Question"].apply(preprocess_text)

# Vectorize the processed CLO descriptions
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(clos_df["Processed_Description"])


# Define route for processing user input and returning result
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    question = data["question"]

    # Preprocess the user's input
    processed_question = preprocess_text(question)

    # Vectorize the processed question using the existing TF-IDF vectorizer
    input_tfidf = vectorizer.transform([processed_question])

    # Calculate similarity between the input question and each CLO description
    similarity_scores = cosine_similarity(input_tfidf, tfidf_matrix)

    # Find the CLO with the highest similarity score
    most_relevant_index = similarity_scores.argmax(axis=1)
    most_relevant_clo = clos_df.loc[most_relevant_index, "CLO"].values[0]

    return jsonify({"clo": most_relevant_clo})


# Define route for serving Sort.jsx
@app.route("/Sort")
def sort():
    return render_template("Sort.jsx")


# Define route for serving Result.jsx
@app.route("/Result")
def result():
    return render_template("Result.jsx")


if __name__ == "__main__":
    app.run(debug=True, port=1800)
