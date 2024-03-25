import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# 1. Load the dataset
try:
    data = pd.read_csv('../data/output/resume_summary.csv')
except FileNotFoundError as e:
    print("File not found:", e)
except KeyError as e:
    print("Missing columns:", e)
    # Print column names to identify the issue
    print("Available columns:", data.columns)

# 2. Data preprocessing
# Assuming the dataset contains two columns: 'resume_text' and 'label'
X = data['text']
y = data['label']

# 3. Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Feature extraction
vectorizer = TfidfVectorizer(max_features=1000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 5. Model training
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# 6. Model evaluation
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification report:\n", report)

print("Saving model to ../data/model/model.pkl")
joblib.dump(model, '../data/model/model.pkl')
