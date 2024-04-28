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

# Vectorizer for CLO descriptions
vectorizer = TfidfVectorizer()


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


# Define route for processing user input and returning result
@app.route("/predict", methods=["POST"])
def predict():
    # Get data from frontend
    data = request.get_json()
    clos_separated = data["closDescription"].split("\n")
    questions_separated = data["question"].split("\n")

    # Convert data to DataFrames
    clo_numbers = []
    clo_descriptions = []
    # Split the CLOs list into separate columns
    for clo in clos_separated:
        split_clo = clo.split(", ")
        clo_numbers.append(split_clo[0])
        clo_descriptions.append(split_clo[1])

    clos_df = pd.DataFrame(({"CLO": clo_numbers, "Description": clo_descriptions}))
    questions_df = pd.DataFrame(({"Question": questions_separated}))

    # Preprocess the data
    clos_df["Processed_Description"] = clos_df["Description"].apply(preprocess_text)
    questions_df["Processed_Question"] = questions_df["Question"].apply(preprocess_text)

    # Vectorize the processed CLO descriptions
    tfidf_matrix = vectorizer.fit_transform(clos_df["Processed_Description"])

    # Vectorize the processed question using the existing TF-IDF vectorizer
    input_tfidf = vectorizer.transform(questions_df["Processed_Question"])

    # Calculate similarity between the input question and each CLO description
    similarity_scores = cosine_similarity(input_tfidf, tfidf_matrix)

    questions_df["Most_Relevant_CLO"] = similarity_scores.argmax(axis=1)
    questions_df["Most_Relevant_CLO"] = questions_df["Most_Relevant_CLO"].apply(
        lambda x: clos_df["CLO"][x]
    )

    questions_dict = questions_df.set_index("Question")["Most_Relevant_CLO"].to_dict()

    # Construct the complaint JSON response
    response = {"questions": questions_dict}

    return jsonify(response)


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
