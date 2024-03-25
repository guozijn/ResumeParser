import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Load model
model = joblib.load('../data/model/model.pkl')

# Read the CSV file containing resume texts
data = pd.read_csv('../data/input/resumes.csv')

# Assuming the 'resume_text' column contains the resume texts
resumes = data['text']

# Initialize the vectorizer
vectorizer = TfidfVectorizer(max_features=193)

# Fit the vectorizer and transform the text data
X = vectorizer.fit_transform(resumes)

# Predict for each resume
for i, resume in enumerate(resumes):
    # Predict
    prediction = model.predict(X[i])

    # Explain the prediction result
    if prediction == 1:
        print("This resume passed the screening.")
    else:
        print("This resume failed the screening.")
