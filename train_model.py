import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # Remove special characters but KEEP numbers and spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    print("Loading IFND.csv...")
    df = pd.read_csv('dataset/IFND.csv', encoding='latin-1')
    
    print(f"Dataset Size: {len(df)}")
    
    # Map labels
    df['Label_num'] = df['Label'].astype(str).str.upper().map({'TRUE': 1, 'FAKE': 0})
    # Drop NaNs in labels just in case
    df = df.dropna(subset=['Label_num'])
    
    # Text preprocessing
    print("Cleaning text (preserving numbers)...")
    df['clean_text'] = df['Statement'].apply(clean_text)
    
    print(f"\nLabel Distribution:\n{df['Label'].value_counts()}\n")

    X = df['clean_text']
    y = df['Label_num']
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Vectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Models to train
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Naive Bayes": MultinomialNB(),
        "SVM": LinearSVC(random_state=42, max_iter=2000, dual=False)
    }
    
    best_model_name = "SVM"
    best_model = None
    
    for name, model in models.items():
        print("-" * 60)
        print(name)
        print("-" * 60)
        
        model.fit(X_train_tfidf, y_train)
        y_pred = model.predict(X_test_tfidf)
        
        acc = accuracy_score(y_test, y_pred) * 100
        prec = precision_score(y_test, y_pred) * 100
        rec = recall_score(y_test, y_pred) * 100
        f1 = f1_score(y_test, y_pred) * 100
        cm = confusion_matrix(y_test, y_pred)
        
        print(f"Accuracy  : {acc:.2f}%")
        print(f"Precision : {prec:.2f}%")
        print(f"Recall    : {rec:.2f}%")
        print(f"F1 Score  : {f1:.2f}%")
        print("\nConfusion Matrix:")
        print(cm)
        print()
        
        if name == best_model_name:
            best_model = model

    print("-" * 60)
    print("Select SVM as best model")
    print("-" * 60)
    
    import os
    if not os.path.exists("models"):
        os.makedirs("models")
        
    print("Saving model and vectorizer...")
    joblib.dump(best_model, 'models/fake_news_model.pkl')
    joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')
    print("Models saved successfully.")

if __name__ == "__main__":
    main()
